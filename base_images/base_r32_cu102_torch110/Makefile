build:
	docker build . -t $$(basename $$(pwd)):latest

run:
	docker run -it --rm --runtime nvidia -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix -v "$$(pwd)/wheels/:/root/Downloads/pytorch/dist"  $$(basename $$(pwd)):latest
