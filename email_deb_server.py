from smtpd import DebuggingServer
import asyncore

deb_server = DebuggingServer(("127.0.0.1",25), None)

print "Starting Debugging Mail Server..."
asyncore.loop()

