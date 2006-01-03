#ifndef STATE_HPP_SENTRY
#define STATE_HPP_SENTRY

bool always_true();
bool always_false();

bool linux_partition_exists();
bool mountpoint_mounted(const ScriptVariable &mp);
bool owl_dir_mounted();
bool active_swap_exists();

void enumerate_owl_dirs(class ScriptVector &dirs,
                        class ScriptVector &parts,
                        bool remove_prefix = true);
void enumerate_owl_dirs3(class ScriptVector &dirs,
                         class ScriptVector &parts,
                         class ScriptVector &types,
                         bool remove_prefix = true);

void enumerate_linux_partitions(class ScriptVector &parts);

void enumerate_active_swaps(class ScriptVector &swaps);
void enumerate_swap_partitions(class ScriptVector &parts);

bool is_mounted(class ScriptVariable &part);

bool packages_installed();
bool keyboard_selected();
bool root_password_set();
bool fstab_exists();
bool fstab_contains_root();
bool timezone_selected();
bool network_configured();
bool can_install_kheaders();
bool kheaders_installed();
bool kernel_installed();

bool minimal_install_ready();


ScriptVariable get_runlevel();


#endif
