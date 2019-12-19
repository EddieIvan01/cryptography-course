# Final

## Mixed encryption (HTTPS)


```
$ python communicate.py server
listent at 127.0.0.1 9999
recv connect from 127.0.0.1 18286
generate RSA key
E: 65537
D: 6062707580700023184695100000054730939031287358333091666734234167494735153690131497468715074963632957897679933816230305636250857311337307284032015698431890901315488605483595523226181341764285343635274481907555848669866608893992736046998363755630496631968724223559244082925741080017998956244851706338733467434513385848074803316227206180555010907515451921672770447843835894182210249455911349926011367875078485445069094904258827301653367501245989301427467577354999278834274209877300835347638041848766639480501378478531121656827394833943613645002060419728973092232910713857007756412047765370205969409858799779105481582865
N: 20088561945312574925697091293977799764967565579810699659374159696400346719621323016816177757616240111317066071212613657944434624380055266063684019051930372314045865652337246564825028899095301509976489393840714275457659535218443902235306727612758777378499129351301996029258521318627817260499461361965800862291391006066493060175326322507966409534043425298158555660658602585043852331613884452589634968805860727634912645968535044064363464896660423581085065027564691286697585421824455097993716633213248957773057145897538797941362834910247280276713635982417178167707521366288617128962147986571893813933020061570450168246657
sending E and N...
recv encrypted file and AES key
decrypt AES key...
AES key is a9b36a0da6b40f16579f6e83424a30b4
decrypt encrypted file with AES key
the file's content is: 
this is the secret file.
```

```
$ python communicate.py client
connect to 127.0.0.1 9999
recv E: 65537
recv N: 20088561945312574925697091293977799764967565579810699659374159696400346719621323016816177757616240111317066071212613657944434624380055266063684019051930372314045865652337246564825028899095301509976489393840714275457659535218443902235306727612758777378499129351301996029258521318627817260499461361965800862291391006066493060175326322507966409534043425298158555660658602585043852331613884452589634968805860727634912645968535044064363464896660423581085065027564691286697585421824455097993716633213248957773057145897538797941362834910247280276713635982417178167707521366288617128962147986571893813933020061570450168246657
generate random AES key: a9b36a0da6b40f16579f6e83424a30b4
encrypt secret.enc with AES128...
sending encrypted file
sending encrypted AES key...
secret file transfering ok
```