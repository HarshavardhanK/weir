output "cluster_endpoint" {
    description = "The endpoint of the EKS cluster"
    value = aws_eks_cluster.weir_cluster.endpoint
}

output "cluster_security_group_id" {
  description = "The security group ID of the EKS cluster"
  value       = aws_eks_cluster.weir_cluster.vpc_config[0].cluster_security_group_id
}