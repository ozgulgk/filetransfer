import pexpect
import signal


################### Error codes used in the sftp module ###################

SUCCESS = 0
SERVER_NOT_CONNECTED_EOF = 1
SERVER_NOT_CONNECTED_TIMEOUT = 2
PUT_ERROR_EOF = 3
PUT_ERROR_TIMEOUT = 4
GET_ERROR_EOF = 5
GET_ERROR_TIMEOUT = 6
UNEXPECTED_ERROR = 7
RM_ERROR_EOF = 8
RM_ERROR_TIMEOUT = 9


error_codes_mapping = (
                   (0, "Success"),
                   (1, "Server Not Connected EOF"),
                   (2, "Server Not Connected TIMEOUT"),
                   (3, "Could Not Put File EOF"),
                   (4, "Could Not Put File TIMEOUT"),
                   (5, "Could Not Get File EOF"),
                   (6, "Could Not Get File TIMEOUT"),
                   (7, "Unexpected Error"),
                   (8, "Could Not Remove File EOF"),
                   (9, "Could Not Remove File TIMEOUT"),
                )

##############################################################################


class FileTransfer:
    "This Class transfers files from/to a server with SFTP"

    command_prompt = "sftp>"


    def __init__(self, source_file, ip_address, port, user, password, server_file_name):

        self.source_file = source_file
        self.ip_address = ip_address
        self.port = port
        self.user = user
        self.password = password
        self.server_file_name = server_file_name
        self.connected_to_server = False
        self.connection = None


    def __del__(self):
        # send exit for SFTP connection
        if self.connected_to_server:
            self.connection.kill(signal.SIGKILL)


    # The following function puts the source_file to target_file in Server by
    # using SFTP.
    def put_file_to_server(self):

        connect_command = 'sftp -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no -oPort=%s %s@%s' % (self.port, 
                                                                                                              self.user, 
                                                                                                              self.ip_address)

        self.connection = pexpect.spawn(connect_command)

        # Expect the line asking password
        index = self.connection.expect(['[pP]assword: ',pexpect.EOF, pexpect.TIMEOUT], timeout=60)

        if index == 0:
            # Send the password
            self.connection.sendline(self.password)
            
            index2 = self.connection.expect([self.command_prompt, pexpect.EOF, pexpect.TIMEOUT],timeout=60)
            if index2 == 0:
                self.connected_to_server = True
            elif index2 == 1:
                return SERVER_NOT_CONNECTED_EOF
            elif index2 == 2:
                return SERVER_NOT_CONNECTED_TIMEOUT
            else:
                return UNEXPECTED_ERROR
        elif index == 1:
            # End Of File exception occurred. Exited from Blackbox
            return SERVER_NOT_CONNECTED_EOF
        elif index == 2:
            # Timeout occurred, SFTP Connection cannot be established
            return SERVER_NOT_CONNECTED_TIMEOUT
        else:
            # Unexpected error
            return UNEXPECTED_ERROR

        if self.connected_to_server:

            put_command = "put %s %s" % (self.source_file, self.server_file_name)
            self.connection.sendline(put_command)

            index = self.connection.expect([self.command_prompt, pexpect.EOF, pexpect.TIMEOUT], timeout=600)
            if index == 0:
                # Exit from Blackbox
                self.connection.kill(signal.SIGKILL)
                self.connected_to_server = False
                return SUCCESS
            elif index == 1:
                # End Of File exception occurred. Exited from Blackbox
                self.connection.kill(signal.SIGKILL)
                self.connected_to_server = False
                return PUT_ERROR_EOF
            elif index == 2:
                # Timeout occurred, no answer from the server
                self.connection.kill(signal.SIGKILL)
                self.connected_to_server = False
                return PUT_ERROR_TIMEOUT  
            else:
                # Unexpected error
                self.connection.kill(signal.SIGKILL)
                self.connected_to_server = False
                return UNEXPECTED_ERROR  


    # The following function gets the file from server by
    # using SFTP. The sourceFile should include the file
    # and path information on server.
    def get_file_from_server(self):

        connect_command = 'sftp -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no -oPort=%s %s@%s' % (self.port, 
                                                                                                              self.user, 
                                                                                                              self.ip_address)
        
        self.connection = pexpect.spawn(connect_command)
    
        # Expect the line asking password
        index = self.connection.expect(['[pP]assword: ',pexpect.EOF, pexpect.TIMEOUT], timeout=60)
        
        if index == 0:
            # Send the password
            self.connection.sendline(self.password)

            index2 = self.connection.expect([self.command_prompt, pexpect.EOF, pexpect.TIMEOUT],timeout=60)
            if index2 == 0:
                self.connected_to_server = True
            elif index2 == 1:
                return SERVER_NOT_CONNECTED_EOF
            elif index2 == 2:
                return SERVER_NOT_CONNECTED_TIMEOUT
            else:
                return UNEXPECTED_ERROR
        elif index == 1:
            # End Of File exception occurred. Exited from Blackbox
            return SERVER_NOT_CONNECTED_EOF
        elif index == 2:
            # Timeout occurred, SFTP Connection cannot be established
            return SERVER_NOT_CONNECTED_TIMEOUT
        else:
            # Unexpected error
            return UNEXPECTED_ERROR

        if self.connected_to_server:    

            get_command = "get %s %s" % (self.source_file, self.server_file_name)
            self.connection.sendline(get_command)

            index = self.connection.expect([self.command_prompt, pexpect.EOF, pexpect.TIMEOUT], timeout=600)
            if index == 0:
                # Everything is OK, exit from Blackbox
                self.connection.kill(signal.SIGKILL)
                self.connected_to_server = False
                return SUCCESS 
            elif index == 1:
                # End Of File exception occurred. Exited from Blackbox
                self.connection.kill(signal.SIGKILL)
                self.connected_to_server = False
                return GET_ERROR_EOF
            elif index == 2:
                # Timeout occurred, no answer from the server
                self.connection.kill(signal.SIGKILL)
                self.connected_to_server = False
                return GET_ERROR_TIMEOUT  
            else:
                # Unexpected error
                self.connection.kill(signal.SIGKILL)
                self.connected_to_server = False
                return UNEXPECTED_ERROR


    # server_file_name should include the path and file on server.
    def rm_file_from_server(self):

        connect_command = "sftp -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no -oPort=%s %s@%s" % (self.port, 
                                                                                                              self.user, 
                                                                                                              self.ip_address)

        self.connection = pexpect.spawn(connect_command)
   
        # Expect the line asking password
        index = self.connection.expect(['[pP]assword: ',pexpect.EOF, pexpect.TIMEOUT], timeout=60)
        
        if index == 0:
            # Send the password
            self.connection.sendline(self.password)

            index2 = self.connection.expect([self.command_prompt, pexpect.EOF, pexpect.TIMEOUT],timeout=60)
            if index2 == 0:
                self.connected_to_server = True
            elif index2 == 1:
                return SERVER_NOT_CONNECTED_EOF
            elif index2 == 2:
                return SERVER_NOT_CONNECTED_TIMEOUT
            else:
                return UNEXPECTED_ERROR
        elif index == 1:
            # End Of File exception occurred. Exited from Blackbox
            return SERVER_NOT_CONNECTED_EOF
        elif index == 2:
            # Timeout occurred, SFTP Connection cannot be established
            return SERVER_NOT_CONNECTED_TIMEOUT
        else:
            # Unexpected error
            return UNEXPECTED_ERROR

        if self.connected_to_server:    

            rm_command = "rm %s" % (self.server_file_name)
            self.connection.sendline(rm_command)

            index = self.connection.expect([self.command_prompt, pexpect.EOF, pexpect.TIMEOUT], timeout=600)
            if index == 0:
                # Everything is OK, exit from Blackbox
                self.connection.kill(signal.SIGKILL)
                self.connected_to_server = False
                return SUCCESS 
            elif index == 1:
                # End Of File exception occurred. Exited from Blackbox
                self.connection.kill(signal.SIGKILL)
                self.connected_to_server = False
                return RM_ERROR_EOF
            elif index == 2:
                # Timeout occurred, no answer from the server
                self.connection.kill(signal.SIGKILL)
                self.connected_to_server = False
                return RM_ERROR_TIMEOUT  
            else:
                # Unexpected error
                self.connection.kill(signal.SIGKILL)
                self.connected_to_server = False
                return UNEXPECTED_ERROR


