

tag=$1

if [ -z "$my_var" ]
then
    tag='latest'
fi

docker build -t hp_analyser:$tag .