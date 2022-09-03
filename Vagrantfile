# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"

  config.vm.synced_folder "app/", "/home/vagrant/app/", create: true

  config.vm.network "private_network", ip: "192.168.56.111"

  config.vm.network "forwarded_port", guest: 80, host: 5011

  config.vm.provision :ansible do |ansible|
    ansible.config_file = "ansible/ansible.cfg"
    ansible.playbook = "ansible/playbook.yml"
    ansible.inventory_path = "ansible/hosts.ini"
    ansible.limit = "development"
    ansible.verbose = "v"
  end

  config.vm.provider "virtualbox" do |v|
    v.linked_clone = true
  end

end
