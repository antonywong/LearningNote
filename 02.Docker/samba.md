sudo docker search samba
sudo docker pull dperson/samba

sudo mkdir /mnt/md0/samba
sudo chmod 777 /mnt/md0/samba

sudo docker run -d --name samba -p 139:139 -p 445:445 \
    -v /mnt/md0/samba:/mount \
    --restart=always dperson/samba \
    -u "wangyj;7" \
    -s "shared;/mount/;yes;no;no;all;none"

sudo docker rm samba -f


Options (fields in '[]' are optional, '<>' are required):
    -h          This help
    -c "<from:to>" setup character mapping for file/directory names
                required arg: "<from:to>" character mappings separated by ','
    -G "<section;parameter>" Provide generic section option for smb.conf
                required arg: "<section>" - IE: "share"
                required arg: "<parameter>" - IE: "log level = 2"
    -g "<parameter>" Provide global option for smb.conf
                required arg: "<parameter>" - IE: "log level = 2"
    -i "<path>" Import smbpassword
                required arg: "<path>" - full file path in container
    -n          Start the 'nmbd' daemon to advertise the shares
    -p          Set ownership and permissions on the shares
    -r          Disable recycle bin for shares
    -S          Disable SMB2 minimum version
    -s "<name;/path>[;browse;readonly;guest;users;admins;writelist;comment]"
                Configure a share
                required arg: "<name>;</path>"
                <name> is how it's called for clients
                <path> path to share
                NOTE: for the default values, just leave blank
                [browsable] default:'yes' or 'no'
                [readonly] default:'yes' or 'no'
                [guest] allowed default:'yes' or 'no'
                NOTE: for user lists below, usernames are separated by ','
                [users] allowed default:'all' or list of allowed users
                [admins] allowed default:'none' or list of admin users
                [writelist] list of users that can write to a RO share
                [comment] description of share
    -u "<username;password>[;ID;group;GID]"       Add a user
                required arg: "<username>;<passwd>"
                <username> for user
                <password> for user
                [ID] for user
                [group] for user
                [GID] for group
    -w "<workgroup>"       Configure the workgroup (domain) samba should use
                required arg: "<workgroup>"
                <workgroup> for samba
    -W          Allow access wide symbolic links
    -I          Add an include option at the end of the smb.conf
                required arg: "<include file path>"
                <include file path> in the container, e.g. a bind mount