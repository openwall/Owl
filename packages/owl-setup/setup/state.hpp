#ifndef STATE_HPP_SENTRY
#define STATE_HPP_SENTRY

bool always_true();
bool always_false();

bool linux_partition_exists();
bool owl_dir_mounted();
bool active_swap_exists();

void enumerate_owl_dirs(class ScriptVector &dirs, class ScriptVector &parts);
void enumerate_owl_dirs3(class ScriptVector &dirs,
                         class ScriptVector &parts,
                         class ScriptVector &types);

void enumerate_linux_partitions(class ScriptVector &parts);

void enumerate_active_swaps(class ScriptVector &swaps);
void enumerate_swap_partitions(class ScriptVector &parts);

bool is_mounted(class ScriptVariable &part);

bool packages_installed();
bool keyboard_selected();
bool root_password_set();
bool fstab_exists();
bool timezone_selected();
bool network_configured();
bool kernel_installed();

ScriptVariable get_runlevel();


#endif
