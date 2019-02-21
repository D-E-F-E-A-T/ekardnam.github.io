
Yeah reader, I know I had promised a post about convolutions last time, but be patient, it's in my TODO list okay?

So I'm here talking about OPSEC and not convolutions, but why? I recently read about a onion website named "Russian Market" being exposed in a tweet by [@ydklijnsma](https://twitter.com/ydklijnsma) and thought I could write something. I'm not gonna talk of the "server side" stuff thought, so if you are a illegal drug market owner and wanna know how to not be catched by the FBI, then this is not the post for you.

I wanna talk about what OPSEC is and give some very basic advices on how to be *a bit* more anonymous while using TOR.

OPSEC stands for OPeration SECurity and it's the process of protection of single pieces of information that, brought together could make a bigger picture on a certain situation or person. OPSEC is all about avoiding people being able to connect those peices of information.

Let's make an example in the TOR context: let's say someone is using an anonymous identity on an IRC network with the nickname Skill3dHAXORX and also a have a social media profile with his name, surname and all sort of personal data. Let's say Skill3dHAXORX is a very bad guy who does steal credit card information and banking data thru malware and phishing and the police have been looking for him for so long, but he uses TOR so he feels safe and anonymous.
Police have been looking at the logs on the servers owned by Skill3dHAX0RX, but just connection from TOR exit nodes are present and can't make a clue. At the same time police log in the IRC channel that Skill3dHAXORX and his companions are writing and uses some social engineering to look like a trustworth blackhat who wants to make loads of money with Skill3dHAXORX and his friends.
After time talking police notices that Skill3dHAXORX uses a very unusual catchphrase when he gets angry at someone, let's say he shouts "FCK U STUPID DUMB VELOCIRAPTOR". Police looks on social media for people who use this kind of phrase and along with info they gathered by talking to Skill3dHAXORX they identify some social media profiles that can match the info they have.
In the morning Skill3dHAXORX finds the cops at home and they find out compromising stuff on his laptop, busted.

The story was very stupid and unrealistic, but you can notice how a single catchphrase can get you deanonymized. Some little information brought together can get you busted.

NEVER EVER user catchphrases, change your way of talking every time you can, never use always same emojis, all of this can get you deanonymized.

Another important thing is NEVER EVER give out personal information via TOR, use a different browser than your usual when using TOR as cookies can be used to deanonymize you and do not login to personal accounts while using TOR.

Keep your sensitive data in an encrypted partition on your drive so it's safe.

Be careful on what goes thru TOR and what does not, take a look at my project [anonymize.sh](https://git.lattuga.net/ekardnam/anonymize.sh).

Have common sense first and then learn all the computer science behind TOR so you can know what can be used to deanonymize you.

ALWAYS USE HTTPS while using TOR, loads of exit nodes are injecting malicious JavaScript in webpages or malicious code in executable you download thru TOR, that can be an exposure to deanonymization.

NEVER EVER TORRENT THRU TOR torrent and TOR do not really work good together, don't mix them.

USE COMMON SENSE, don't send a mail with terrorist alert to your town's major from you town hall's public wifi thru TOR as a joke. Take a book about good jokes and think, you are gonna be the only one using TOR in the day the mail was sent on the hall's wifi, wouldn't they notice?