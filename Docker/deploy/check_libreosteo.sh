check_root() {
	if ! id -u | grep -q '^0$'
	then
		echo "Please launch the script on root, maybe sudo $0"
		exit 1
	fi
}

check_docker() {
	if ! which docker > /dev/null
	then
		echo "Please install docker, see https://docs.docker.com/install/#server"
		exit 1
	fi
}

check_docker_compose() {
	if ! which docker-compose > /dev/null
	then
		echo "Please install docker-compose, see https://docs.docker.com/compose/install/#install-compose"
		exit 1
	fi
}

check_rank_lo() {
	if [[ -d $LO_DIR/$rank ]]
	then
		echo "Please use another rank, it already exist, for example: $0 preprod 8086"
		exit 1
	fi
}

check_rm_rank_lo() {
	if [[ ! -d $LO_DIR/$rank ]]
	then
		ranks="$(ls $LO_DIR)"
		echo "The rank doesn't exist, possible ranks:"
		echo "$ranks"
		exit 1
	fi
}

check_port_lo() {
	if wget localhost:$port -o /dev/null
	then
		echo "Please use another port, for example: $0 $rank 8086"
		exit 1
	fi
}

check_install_all() {
	check_root
	check_docker
	check_docker_compose
	check_rank_lo
	check_port_lo
}

check_remove_all() {
	check_root
	check_docker
	check_docker_compose
	check_rm_rank_lo
}
