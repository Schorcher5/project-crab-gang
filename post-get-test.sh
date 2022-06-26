#!/bin/bash

DATA="name=Joaquin&email=jo@gmail.com&content=$1"
curl --request POST http://portfoliobuilder.duckdns.org:5000/api/timeline_post -d $DATA
GET=$(curl http://portfoliobuilder.duckdns.org:5000/api/timeline_post | grep -o '"content":"[^"]*' | grep -o '[^"]*$') 

echo $GET

do
	if [ $ENTRY = $1 ]
	then
		echo "Successful post"
	fi

done
