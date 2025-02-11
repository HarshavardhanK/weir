variable "region" {
    description = "The AWS Region for the project"
    default = "us-west-2"
}

variable "cluster_name" {
    description = "The name of EKS cluster"
    default = "weir-cluster"
}

variable "node_instance_type" {
    description = "EC2 Instance for Weir"
    default = "t3.medium"
}