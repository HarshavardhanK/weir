resource "aws_vpc" "weir_vpc" {
    cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "weir_subnet" {
    count = 2
    vpc_id = aws_vpc.weir_vpc.id
    cidr_block = cidrsubnet(aws_vpc.weir_vpc.cidr_block, 8, count.index)
    availability_zone = element(data.aws_availability_zones.available.names, count.index)
    map_public_ip_on_launch = true
}

data "aws_availability_zones" "available" {}