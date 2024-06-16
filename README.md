# Setup

```sh
python3 -m venv venv
source ./venv/bin/activate
pip install -r ./requirements.txt
```

To get started with development:

```sh
## pgvector
https://github.com/pgvector/pgvector

brew install postgresql
mkdir tmp && cd tmp
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make && make install
cd .. && rm -rf tmp

## database
psql postgres
CREATE DATABASE pgvector_example;
```

## Examples

```sh
corpus = [
    "Princess Leia hides the Death Star plans in R2-D2.",
    "Darth Vader captures Princess Leia's ship.",
    "Luke Skywalker discovers a message from Princess Leia in R2-D2.",
    "Luke meets Obi-Wan Kenobi and learns about the Force.",
    "Luke's aunt and uncle are killed by Imperial stormtroopers.",
    "Luke and Obi-Wan hire Han Solo and Chewbacca at Mos Eisley Cantina.",
    "The Millennium Falcon escapes Tatooine and is pursued by Imperial ships.",
    "The Millennium Falcon is captured by the Death Star.",
    "Luke, Han, and Chewbacca rescue Princess Leia.",
    "They escape through the garbage chute and are nearly crushed.",
    "Obi-Wan Kenobi disables the tractor beam.",
    "Obi-Wan Kenobi duels Darth Vader and sacrifices himself.",
    "The Millennium Falcon escapes from the Death Star.",
    "R2-D2 delivers the Death Star plans to the Rebel Alliance.",
    "The Rebels plan an attack on the Death Star.",
    "Luke joins the Rebel fleet as a pilot.",
    "The Rebels begin their attack on the Death Star.",
    "Han Solo returns to help Luke during the attack.",
    "Luke uses the Force to destroy the Death Star.",
    "The Rebels celebrate their victory and honor their heroes.",
    "The Rebels are stationed on the ice planet Hoth.",
    "Imperial forces discover the Rebel base and attack.",
    "Han Solo and Princess Leia escape in the Millennium Falcon.",
    "Luke Skywalker travels to Dagobah to train with Yoda.",
    "Han and Leia evade the Empire and hide in Cloud City.",
    "Darth Vader reveals a trap to capture Luke.",
    "Han Solo is betrayed and frozen in carbonite.",
    "Luke confronts Vader and loses his hand in a lightsaber duel.",
    "Vader reveals that he is Luke's father.",
    "Luke escapes with the help of Leia, Lando, and Chewbacca.",
    "Luke Skywalker and his friends plan to rescue Han Solo.",
    "They infiltrate Jabba the Hutt's palace on Tatooine.",
    "Leia frees Han, but they are captured.",
    "Luke arrives and defeats Jabba's forces.",
    "The group destroys Jabba's sail barge and escapes.",
    "The Rebels plan an attack on the new Death Star.",
    "Luke returns to Dagobah to complete his training.",
    "Yoda dies, and Luke learns Leia is his sister.",
    "The Rebels land on Endor to disable the Death Star's shield generator.",
    "Luke surrenders to Vader to confront the Emperor.",
    "Vader takes Luke to the Emperor on the Death Star.",
    "The Rebels attack the Death Star while ground forces fight on Endor.",
    "Luke refuses to join the dark side and battles Vader.",
    "Vader turns on the Emperor to save Luke.",
    "Vader dies, and the Death Star is destroyed.",
    "The Empire is defeated, and the galaxy celebrates.",
]

Given the Star Wars New Hope episode

Asking: Wer ist mit wem verwandt?

We get answers:

(venv) ➜  ./transformer-pgvector.py
Vader reveals that he is Luke's father.
Yoda dies, and Luke learns Leia is his sister.
Luke meets Obi-Wan Kenobi and learns about the Force.
Luke's aunt and uncle are killed by Imperial stormtroopers.
Vader turns on the Emperor to save Luke.
Imperial forces discover the Rebel base and attack.
The Empire is defeated, and the galaxy celebrates.
Luke Skywalker travels to Dagobah to train with Yoda.
Darth Vader reveals a trap to capture Luke.
Leia frees Han, but they are captured.

Asking: Was ist passiert?

We get answers:

(venv) ➜  ./transformer-pgvector.py
The Empire is defeated, and the galaxy celebrates.
The Millennium Falcon is captured by the Death Star.
Yoda dies, and Luke learns Leia is his sister.
Vader dies, and the Death Star is destroyed.
Vader reveals that he is Luke's father.
They escape through the garbage chute and are nearly crushed.
Imperial forces discover the Rebel base and attack.
The Millennium Falcon escapes from the Death Star.
Leia frees Han, but they are captured.
Luke uses the Force to destroy the Death Star.
```
