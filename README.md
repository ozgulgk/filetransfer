# filetransfer
filetransfer is a simple Python utility which can be used to connect to a server via SFTP.

The following actions can be taken with this utility:
- Get a file from a server via SFTP.
- Put a file to a server via SFTP.
- Remove file from a server via SFTP.

# Usage
- Getting a file from a server:

In [1]: from filetransfer import sftp

In [2]: ft = sftp.FileTransfer("folder_on_server/file_on_server", "172.18.111.80","22","user1","pass1","folder_to_get_the_file/file_name")

In [3]: ft.get_file_from_server()

Out[3]: 0

- Putting a file to a server:

In [1]: from filetransfer import sftp

In [2]: ft = sftp.FileTransfer("folder_to_get_the_file/file_to_be_transferred", "172.18.111.80","22","user1","pass1","folder_on_server/file_name_on_server")

In [3]: ft.put_file_to_server()

Out[5]: 0

- Remove file from a server

In [1]: from filetransfer import sftp

In [2]: ft = sftp.FileTransfer(None, "172.18.111.80","22","user1","pass1","folder_on_server/file_to_be_removed_from_server")

In [3]: ft.rm_file_from_server()

Out[3]: 0


