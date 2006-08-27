#include <stdio.h>
#include <unistd.h>
#include <ctype.h>
#include <sys/types.h>
#include <sys/stat.h>

#include "scriptpp/scrvar.hpp"
#include "scriptpp/scrvect.hpp"

#include "ip4areas/ip4areas.hpp"

#include "cmd.hpp"
#include "iface.hpp"
#include "config.hpp"


class NetconfInfo {
    ScriptVariable hostname;
    struct Iface {
        ScriptVariable name;
        IP4IpAddress ip;
        IP4Mask mask;
        Iface *next;
        Iface(const ScriptVariable &a_name,
              const IP4IpAddress &a_ip,
              const IP4Mask &a_mask)
            : name(a_name), ip(a_ip), mask(a_mask), next(0) {}
    } *first_iface;
    IP4IpAddress gateway;
    bool forward_ipv4;
    struct DnsIp {
        IP4IpAddress ip;
        DnsIp *next;
    } *first_dns;

    ScriptVector deleted_interfaces;

public:
    NetconfInfo() { first_iface = 0; first_dns = 0;
                    forward_ipv4 = false; AddLoopback(); }
    ~NetconfInfo() {
        DropInterfaces();
        ClearDns();
    }

    bool SetHostname(const ScriptVariable &a) {
        if(a=="") { hostname = ""; return true; }
        ScriptVector h(a, ".", "");
        for(int i=0; i<h.Length(); i++) {
            if(h[i]=="") return false; // smth like "host..domain" is invalid
            for(int j=0; j<h[i].Length(); j++) {
                char c = h[i][j];
                if(!isascii(c)) return false;
                if(!isalnum(c) && c != '-') return false;
            }
        }
        hostname = a;
        return true;
    }

    void ClearInterfaces() {
        DropInterfaces();
        AddLoopback();
    }
    bool AddInterface(const ScriptVariable& a_name,
                      const ScriptVariable& a_ip,
                      const ScriptVariable& a_mask)
    {
        IP4IpAddress ip(a_ip.c_str());
        IP4Mask mask(a_mask.c_str());
        if(ip.IsInvalid() || mask.IsInvalid()) return false;
        for(Iface *p = first_iface; p; p=p->next) {
            if(p->name == a_name) {
                p->ip = ip;
                p->mask = mask;
                return true;
            }
        }
        Iface *p = new Iface(a_name, ip, mask);
        p->next = first_iface;
        first_iface = p;
        return true;
    }
    void AddLoopback() { AddInterface("lo", "127.0.0.1", "/8"); }

    bool SetGateway(const ScriptVariable &a_gw) {
        IP4IpAddress gw(a_gw.c_str());
        if(gw.IsInvalid())
            return false; /* invalid gw, e.g. not an ip-address */
        if(!GetIfaceByReachableIp(gw))
            return false; /* unreachable gw */
        gateway = gw;
        return true;
    }

    bool AddDns(const ScriptVariable &a_dns) {
        IP4IpAddress ip(a_dns.c_str());
        if(ip.IsInvalid())
            return false; /* invalid ip-address */
        DnsIp** p;
        for(p = &first_dns; *p; p=&((*p)->next)) {
            if((*p)->ip == ip) return true;
        }
        *p = new DnsIp;
        (*p)->ip = ip;
        (*p)->next = 0;
        return true;
    }

    void ClearDns() {
        while(first_dns) {
            DnsIp *tmp = first_dns;
            first_dns = first_dns->next;
            delete tmp;
        }
    }

    void SetForwarding(bool a) { forward_ipv4 = a; }

    // --------------------------------------------------------------

    const ScriptVariable GetFullHostname() const {
        return hostname == "" ? "localhost" : hostname;
    }
    ScriptVariable GetShortHostname() const {
        if(hostname == "") return "localhost";
        ScriptVariable::Substring w;
        ScriptVariable hn(hostname);
        hn.Whole().FetchToken(w, ".");
        return w.Get();
    }
    ScriptVariable GetDomain() const {
        if(hostname == "") return "localdomain";
        ScriptVariable::Substring h, d;
        ScriptVariable hn(hostname);
        d = hn.Whole();
        d.FetchToken(h, ".");
        return d.Get();
    }

    class IfaceIterator;
    friend class NetconfInfo::IfaceIterator;

    class IfaceIterator {
        NetconfInfo::Iface *p;
    public:
        IfaceIterator(const NetconfInfo& master) { p = master.first_iface; }
        operator bool() { return p!=0; }
        void Next() { p = p->next; }
        ScriptVariable Name() const { return p->name; }
        ScriptVariable Ip() const { return p->ip.TextForm(); }
        ScriptVariable Mask() const { return p->mask.LongTextForm(); }
        ScriptVariable Network() const {
            return IP4Subnet(p->ip, p->mask).First().TextForm();
        }
        ScriptVariable Broadcast() const {
            return IP4Subnet(p->ip, p->mask).Last().TextForm();
        }
    };

    bool InterfaceExists(const ScriptVariable& nm) const {
        for(Iface *p = first_iface; p; p=p->next) {
            if(p->name == nm) return true;
        }
        return false;
    }

    bool GetInterfaceInfo(const ScriptVariable& name,
                          ScriptVariable &ip,
                          ScriptVariable &mask) const
    {
        for(Iface *p = first_iface; p; p=p->next) {
            if(p->name == name) {
                ip = p->ip.TextForm();
                mask = p->mask.TextForm();
                return true;
            }
        }
        return false;
    }

    bool RemoveInterface(const ScriptVariable& name) {
        if(name == "lo") return false;
        for(Iface **p = &first_iface; *p; p=&((*p)->next)) {
            if((*p)->name == name) {
                Iface *tmp = *p;
                *p = tmp->next;
                delete tmp;
                deleted_interfaces.AddItem(name);
                return true;
            }
        }
        return false;
    }

    const ScriptVector& RemovedInterfaces() const {
        return deleted_interfaces;
    }

    ScriptVariable GetGateway() const { return gateway.TextForm(); }

    void GetDnsServers(ScriptVector &v) const {
        v.Clear();
        for(DnsIp *p = first_dns; p; p = p->next)
            v.AddItem(p->ip.TextForm());
    }

    bool IsForwardingEnabled() const { return forward_ipv4; }

    ScriptVariable GatewayIface() const {
        Iface *p = GetIfaceByReachableIp(gateway);
        return p ? p->name : "???";
    }

    ScriptVariable MainIpAddress() const {
        for(Iface *p = first_iface; p; p=p->next) {
            if(p->name != "lo") return p->ip.TextForm();
        }
        // not found...
        return "127.0.0.1";
    }

    ScriptVariable GuessGateway() const {
        for(Iface *p = first_iface; p; p=p->next) {
            if(p->name != "lo") {
                IP4Subnet sub(p->ip, p->mask);
                IP4IpAddress ip(sub.First());
                ip++;
                return ip.TextForm();
            }
        }
        // not found...
        return "";

    }

private:
    Iface* GetIfaceByReachableIp(const IP4IpAddress &ip) const {
        for(Iface *p = first_iface; p; p=p->next) {
            if(IP4Subnet(p->ip, p->mask).Contains(ip)) {
                return p;
            }
        }
        return 0;
    }
    void DropInterfaces() {
        while(first_iface) {
            Iface *tmp = first_iface;
            first_iface = first_iface->next;
            delete tmp;
        }
    }

    NetconfInfo(const NetconfInfo &) {} // no copying for such a monster
};


static void scan_net_config(NetconfInfo &info)
{
    if(the_config->OwlRoot()!="" &&
       the_config->OwlRoot()!="/" &&
       !FileStat(the_config->NetworkSysconf().c_str()).Exists())
    {
        /* scan the base system's settings... */
        ScriptVariable save_root = the_config->OwlRoot();
        the_config->SetRoot("");
        scan_net_config(info);
        the_config->SetRoot(save_root.c_str());
        return;
    }

    info.ClearDns();
    // read dns servers from resolv.conf
    {
        ReadText resolv(the_config->ResolvFile().c_str());
        ScriptVector v;
        while(resolv.ReadLine(v,2)) {
            if(v[0] == "nameserver") info.AddDns(v[1]);
        }
    }

    // read interfaces information
    info.ClearInterfaces();
    {
        ScriptVariable nsdircfg = the_config->NetworkScriptsDir();
        const char *nsdir = nsdircfg.c_str();
        ReadDir netscripts(nsdir);
        const char *ss;
        while((ss = netscripts.Next())) {
            ScriptVariable s(ss);
            if(s.HasPrefix("ifcfg-")) {
                ScriptVariable devname, ip, mask;
                ScriptVariable fname(0, "%s/%s", nsdir, s.c_str());
                ReadText f(fname.c_str());
                ScriptVector v;
                while(f.ReadLine(v, 2, "=", " \t")) {
                    if(v[0]=="DEVICE") devname = v[1];
                    else
                    if(v[0]=="IPADDR") ip = v[1];
                    else
                    if(v[0]=="NETMASK") mask = v[1];
                }
                info.AddInterface(devname, ip, mask);
            }
        }
    }

    // read general network information
    {
        ReadText net(the_config->NetworkSysconf().c_str());
        ScriptVector v;
        while(net.ReadLine(v, 2, "=", " \t")) {
            if(v[0] == "HOSTNAME") info.SetHostname(v[1]);
            else
            if(v[0] == "GATEWAY") info.SetGateway(v[1]);
#if 0
            else
            if(v[0] == "FORWARD_IPV4") info.SetForwarding(v[1]=="true");
#endif
        }
    }

}

static ScriptVariable summary_net_config(NetconfInfo &info)
{
    ScriptVariable res;
    res += "Hostname:        "; res += info.GetFullHostname(); res += "\n";
    NetconfInfo::IfaceIterator ii(info);
    bool i_p = true;
    while(ii) {
        res += ScriptVariable(0, "%s     %-7s %16s/%s\n",
                     i_p ? "Interfaces: " : "            ",
                     ii.Name().c_str(), ii.Ip().c_str(), ii.Mask().c_str());
        i_p = false;
        ii.Next();
    }
    if(info.GetGateway() == "255.255.255.255") {
        res += "Gateway:         none\n";
    } else {
        res += ScriptVariable(0, "Gateway:         %s (via %s)\n",
                                 info.GetGateway().c_str(),
                                 info.GatewayIface().c_str());
    }

    ScriptVector dns;
    info.GetDnsServers(dns);
    res += "DNS servers:     "; res += dns.Join(", "); res += "\n";
#if 0
    res += "IPv4 forwarding: ";
    res += info.IsForwardingEnabled() ? "enabled" : "disabled";
#endif

    return res;
}

static ScriptVariable summary_net_ifaces(NetconfInfo &info)
{
    ScriptVariable res;
    NetconfInfo::IfaceIterator ii(info);
    while(ii) {
        res += ScriptVariable(0, "%-7s %16s/%s\n",
                   ii.Name().c_str(), ii.Ip().c_str(), ii.Mask().c_str());
        ii.Next();
    }
    return res;
}

static bool save_hosts_file(const NetconfInfo &info,
                            bool append_mode = false)
{
    FILE *f;
    f = fopen(the_config->HostsFile().c_str(), append_mode ? "a" : "w");
    if(f) {
        fchmod(fileno(f), 0644);

        if(!append_mode && info.MainIpAddress() != "127.0.0.1")
            fprintf(f, "127.0.0.1\tlocalhost\n");

        ScriptVariable fullnm(info.GetFullHostname());
        ScriptVariable shortnm(info.GetShortHostname());

        if(fullnm == shortnm) {
            fprintf(f, "%s\t\%s\n",
                       info.MainIpAddress().c_str(),
                       shortnm.c_str());
        } else {
            fprintf(f, "%s\t\%s %s\n",
                       info.MainIpAddress().c_str(),
                       fullnm.c_str(),
                       shortnm.c_str());
        }
        fclose(f);
        return true;
    } else
        return false;
}



static bool save_net_config(const NetconfInfo &info)
{
    FILE* f;
    bool success = true;

    f = fopen(the_config->ResolvFile().c_str(), "w");
    if(f) {
        fchmod(fileno(f), 0644);
        if(info.GetDomain()!="") {
            fprintf(f, "domain %s\nsearch %s\n", info.GetDomain().c_str(),
                                                 info.GetDomain().c_str());
        }
        ScriptVector dns;
        info.GetDnsServers(dns);
        for(int i=0; i<dns.Length(); i++)
            fprintf(f, "nameserver %s\n", dns[i].c_str());
        fclose(f);
    } else
        success = false;

    f = fopen(the_config->NetworkSysconf().c_str(), "w");
    if(f) {
        fchmod(fileno(f), 0600);
        fprintf(f, "NETWORKING=yes\n"
#if 0
                   "FORWARD_IPV4=%s\n"
#endif
                   "HOSTNAME=%s\n"
                   "DOMAINNAME=%s\n"
                   "GATEWAY=%s\n"
                   "GATEWAYDEV=%s\n",
#if 0
                   info.IsForwardingEnabled() ? "true" : "false",
#endif
                   info.GetFullHostname().c_str(),
                   info.GetDomain().c_str(),
                   info.GetGateway().c_str(),
                   info.GatewayIface().c_str());
        fclose(f);
    } else
        success = false;

    const ScriptVector &del_ifaces = info.RemovedInterfaces();
    for(int i=0; i<del_ifaces.Length(); i++) {
        ScriptVariable fname(the_config->NetworkScriptsDir());
        fname += "/ifcfg-";
        fname += del_ifaces[i];
        unlink(fname.c_str());
    }

    NetconfInfo::IfaceIterator ii(info);
    while(ii) {
        if(ii.Name() == "lo") {
            ii.Next();
            continue;
        }
        ScriptVariable fname(the_config->NetworkScriptsDir());
        fname += "/ifcfg-";
        fname += ii.Name();
        f = fopen(fname.c_str(), "w");
        if(f) {
            fchmod(fileno(f), 0600);
            fprintf(f, "DEVICE=%s\n"
                       "BOOTPROTO=static\n"
                       "IPADDR=%s\n"
                       "NETMASK=%s\n"
                       "NETWORK=%s\n"
                       "BROADCAST=%s\n",
                       ii.Name().c_str(),
                       ii.Ip().c_str(),
                       ii.Mask().c_str(),
                       ii.Network().c_str(),
                       ii.Broadcast().c_str());
#if 0
            if(ii.Name() == "lo")
                fprintf(f, "NAME=loopback\n");
                       /* I don't know what's this for */
#endif
            fclose(f);
        } else
            success = false;
        ii.Next();
    }

    return success;
}

static bool check_hosts_for_line(NetconfInfo& info)
{
    ScriptVariable mainip(info.MainIpAddress());
    ScriptVariable fullnm(info.GetFullHostname());
    ReadText hosts(the_config->HostsFile().c_str());
    ScriptVector buf;
    while(hosts.ReadLine(buf)) {
        if(buf[0] == mainip && buf[1] == fullnm) return true;
    }
    return false;
}

static bool save_all(OwlInstallInterface* the_iface, NetconfInfo& info)
{
    FileStat hosts(the_config->HostsFile().c_str());
    if(hosts.IsRegularFile() && !hosts.IsEmpty()) {
        if(!check_hosts_for_line(info)) {
            IfaceSingleChoice *pm = the_iface->CreateSingleChoice();
            pm->SetCaption(ScriptVariable("What to do with ")+
                           the_config->HostsFile() + "?");
            pm->AddItem("p", "Explain what it's all about");
            pm->AddItem("i", "Just ignore, I'll update it myself");
            pm->AddItem("o", "Overwrite it, I don't need its contents");
            pm->AddItem("a", "Append the necessary line to the end of file");
            pm->AddItem("c", "Cancel");
            do {
                ScriptVariable choice = pm->Run();
                if(choice == "p") {
                    ScriptVariable msg(0,
                        "There should be a line in your %s which contains:"
                        "\n\n%s %s\n\n"
                        "(your main IP address and your hostname).\n"
                        "There seems to be some content already but\n"
                        "the line above doesn't appear.",
                        the_config->HostsFile().c_str(),
                        info.MainIpAddress().c_str(),
                        info.GetFullHostname().c_str());
                    the_iface->Message(msg);
                    continue;
                } else
                if(choice == "i") {
                    break;
                } else
                if(choice == "o") {
                    if(!save_hosts_file(info)) {
                        the_iface->Message("Problems writing the hosts file");
                        delete pm;
                        return false;
                    }
                    break;
                } else
                if(choice == "a") {
                    if(!save_hosts_file(info, true)) {
                        the_iface->Message("Problems writing the hosts file");
                        delete pm;
                        return false;
                    }
                    break;
                } else
                if(choice == "c") {
                    delete pm;
                    return false;
                }
            } while(true);
            delete pm;
        } else {
            // the necessary line seems to be there already, do nothing
        }
    } else {
        // hosts doesn't exist or is empty... just overwrite it, no asking
        if(!save_hosts_file(info)) {
            the_iface->Message("Problems writing the hosts file");
        }
    }
    if(!save_net_config(info)) {
        the_iface->Message("Problems saving the network configuration");
        return false;
    }
    the_iface->Message("Network configuration saved");
    return true;
}

static bool query_ip_and_mask(OwlInstallInterface *the_iface,
                            ScriptVariable &ip, ScriptVariable &mask)
{
    ScriptVariable newip =
        the_iface->QueryString("Enter IP address", ip, false);
    if(newip == OwlInstallInterface::qs_cancel) return false;
    if(IP4IpAddress(newip.c_str()).IsInvalid()) {
        the_iface->Message("Invalid IP address");
        return false;
    }

    ScriptVariable newmask =
        the_iface->QueryString("Enter netmask (e.g., /24 or 255.255.255.0)",
                               mask, false);
    if(newmask == OwlInstallInterface::qs_cancel) return false;
    if(IP4Mask(newmask.c_str()).IsInvalid()) {
        the_iface->Message("Invalid netmask");
        return false;
    }

    ip = newip;
    mask = newmask;
    return true;
}

static ScriptVariable
choose_existing_interface(OwlInstallInterface* the_iface,
                          const NetconfInfo &info)
{
    IfaceSingleChoice *pm = the_iface->CreateSingleChoice();
    pm->SetCaption("Select interface");
    NetconfInfo::IfaceIterator ii(info);
    int n = 0;
    while(ii) {
        if(ii.Name()!="lo") {
            pm->AddItem(ii.Name(), ii.Name());
            n++;
        }
        ii.Next();
    }
    pm->AddItem("q", "Quit/cancel");
    if(n == 0) {
        the_iface->Message("No interfaces available");
        delete pm;
        return "";
    }
    ScriptVariable choice = pm->Run();

    delete pm;

    if(choice == "q" ||
       choice == OwlInstallInterface::qs_eof ||
       choice == OwlInstallInterface::qs_escape ||
       choice == OwlInstallInterface::qs_cancel)
    {
        return "";
    }

    return choice;
}

static void edit_interfaces(OwlInstallInterface* the_iface,
                            NetconfInfo& info)
{
    IfaceSingleChoice *pm = the_iface->CreateSingleChoice();
    pm->SetCaption("Network interfaces configuration");
    pm->AddItem("v", "View interfaces");
    pm->AddItem("a", "Add interface");
    pm->AddItem("e", "Edit interface");
    pm->AddItem("r", "Remove interface");
    pm->AddItem("q", "Done, return to network menu");
    do {
        ScriptVariable choice = pm->Run();
        if(choice=="v") {
            the_iface->Message(summary_net_ifaces(info));
        }
        else if(choice=="a") {
            ScriptVariable name =
                the_iface->QueryString("Enter the interface name",
                                       "eth0", false);
            if(name == OwlInstallInterface::qs_eof) return;
            if(name == OwlInstallInterface::qs_cancel) continue;
            if(name == "" || name.Strchr(' ').Valid()) {
                the_iface->Message("Invalid interface name");
                continue;
            }
            if(info.InterfaceExists(name)) {
                the_iface->Message("Interface already exists, try \"edit\"");
                continue;
            }
            ScriptVariable ip, mask;
            if(!query_ip_and_mask(the_iface, ip, mask)) continue;
            info.AddInterface(name, ip, mask);
        }
        else if(choice=="e") {
            ScriptVariable name =
                choose_existing_interface(the_iface, info);
            if(name=="") continue;
            ScriptVariable ip, mask;
            info.GetInterfaceInfo(name, ip, mask);
            if(!query_ip_and_mask(the_iface, ip, mask)) continue;
            info.AddInterface(name, ip, mask);
        }
        else if(choice=="r") {
            ScriptVariable name =
                choose_existing_interface(the_iface, info);
            if(name=="") continue;
            info.RemoveInterface(name);
        }
        else if(choice == "q" ||
                choice == OwlInstallInterface::qs_eof ||
                choice == OwlInstallInterface::qs_escape ||
                choice == OwlInstallInterface::qs_cancel)
        {
            break;
        }
    } while(true);
    delete pm;
}

static void edit_nameservers(OwlInstallInterface* the_iface,
                            NetconfInfo& info)
{
    IfaceSingleChoice *pm = the_iface->CreateSingleChoice();
    pm->SetCaption("DNS servers list");
    pm->AddItem("v", "View list");
    pm->AddItem("a", "Add server");
    pm->AddItem("c", "Clear list");
    pm->AddItem("q", "Done, return to network menu");
    do {
        ScriptVariable choice = pm->Run();
        if(choice=="v") {
            ScriptVector v;
            info.GetDnsServers(v);
            if(v.Length()>0)
                the_iface->Message(v.Join(", "));
            else
                the_iface->Message("No DNS servers set (yet?)");
        }
        else if(choice=="a") {
            ScriptVariable serv =
                the_iface->QueryString("Enter the DNS server's IP address",
                                       false);
            if(serv == OwlInstallInterface::qs_eof)
                break;
            if(serv == OwlInstallInterface::qs_cancel)
                continue;
            if(serv == OwlInstallInterface::qs_escape)
                continue;
            if(!info.AddDns(serv)) {
                the_iface->Message("Invalid IP address");
            }
        }
        else if(choice=="c") {
            info.ClearDns();
        }
        else if(choice == "q" ||
                choice == OwlInstallInterface::qs_eof ||
                choice == OwlInstallInterface::qs_escape ||
                choice == OwlInstallInterface::qs_cancel)
        {
            break;
        }
    } while(true);
    delete pm;
}

void configure_network(OwlInstallInterface *the_iface)
{
    IfaceSingleChoice *pm = the_iface->CreateSingleChoice();
    pm->SetCaption("Network configuration");
    pm->AddItem("v", "View the current settings");
    pm->AddItem("h", "Set hostname");
    pm->AddItem("i", "Edit interfaces");
    pm->AddItem("g", "Set default gateway");
    pm->AddItem("n", "Edit DNS servers");
#if 0
    pm->AddItem("f", "Toggle IPv4 forwarding");
#endif
    pm->AddItem("s", "Save and return to main menu");
    pm->AddItem("x", "Return to main menu without saving");
    NetconfInfo info;
    scan_net_config(info);
    do {
        ScriptVariable choice = pm->Run();
        if(choice=="") continue;
        else if(choice=="v") {
            the_iface->Message(summary_net_config(info));
        }
        else if(choice=="h") {
            ScriptVariable res =
                the_iface->QueryString("Enter the fully-qualified hostname",
                                       info.GetFullHostname(), false);
            if(res == OwlInstallInterface::qs_eof) {
                return;
            }
            if(res != OwlInstallInterface::qs_cancel) {
                info.SetHostname(res);
            }
        }
        else if(choice=="i") {
            edit_interfaces(the_iface, info);
        }
        else if(choice=="g") {
            ScriptVariable res =
                the_iface->QueryString("Enter your gateway IP address",
                                       info.GuessGateway(), false);
            if(res == OwlInstallInterface::qs_eof) {
                return;
            }
            if(res != OwlInstallInterface::qs_cancel) {
                if(!info.SetGateway(res)) {
                     the_iface->Message("Gateway address is invalid or "
                                        "it is not reachable via known "
                                        "interfaces");
                }
            }
        }
        else if(choice=="n") {
            edit_nameservers(the_iface, info);
        }
#if 0
        else if(choice=="f") {
            bool ena = !info.IsForwardingEnabled();
            info.SetForwarding(ena);
            the_iface->Message(ScriptVariable("IPv4 forwarding is ") +
                              ScriptVariable(ena ? "enabled" : "disabled"));
        }
#endif
        else if(choice=="s") {
            if(save_all(the_iface, info))
                break;
        }
        else if(choice == "x" ||
                choice == OwlInstallInterface::qs_escape ||
                choice == OwlInstallInterface::qs_cancel)
        {
            if(the_iface->YesNoMessage("Really quit without saving?")) break;
        }
        else if(choice == OwlInstallInterface::qs_eof)
        {
            break;
        }
    } while(1);
    delete pm;
}
