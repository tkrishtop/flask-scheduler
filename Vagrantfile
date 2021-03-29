Vagrant.configure("2") do |config|
  config.vm.provider "virtualbox" do |vb, override|
    vb.memory = 4096
    vb.cpus = 4
    override.vm.box = "bento/ubuntu-20.04"
  end

  # forward ports
  config.vm.network "forwarded_port", guest: 5555, host: 5555   # flask scheduler
  config.vm.network "forwarded_port", guest: 9090, host: 9090   # prometheus
  config.vm.network "forwarded_port", guest: 9100, host: 9100   # prometheus node
  config.vm.network "forwarded_port", guest: 3000, host: 3000   # grafana

  # post-installation script
  config.vm.provision :shell, :path => "provision.sh"

  # Declare shared folder with Vagrant syntax
  config.vm.synced_folder ".", "/home/vagrant/scheduler", :mount_options => ["dmode=775", "fmode=666"]
end