#include "iface.hpp"

void pam_root_passwd(OwlInstallInterface *the_iface);

void set_root_password(OwlInstallInterface *the_iface)
{
    pam_root_passwd(the_iface);
}
