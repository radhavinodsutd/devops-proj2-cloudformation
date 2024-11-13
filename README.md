# DevOps Beginner Project: Automated Infrastructure Setup and CI/CD with AWS CodeDeploy

## Project Overview
This project focuses on automating infrastructure provisioning, application deployment, and establishing a CI/CD pipeline for a web application using AWS services and GitHub Actions. The key elements include AWS CloudFormation, EC2, RDS, CodeDeploy, Systems Manager (SSM), S3, and GitHub Actions.

## Project Steps

### Step 1: Create the CloudFormation Template
1. **Create a CloudFormation YAML file** that defines the following resources:
    - **VPC, Subnets, Internet Gateway, Route Table** for networking.
    - **EC2 Instances** with an **SSM-supported AMI** (Amazon Linux 2).
      - Ensure the instances have:
        - **Tags** for identification (`Environment=Production`).
        - **IAM Role** with the following policies:
          - `AmazonSSMManagedInstanceCore` for Systems Manager.
          - `AWSCodeDeployRole` for CodeDeploy access.
    - **RDS Instance** for the database with appropriate security groups.
    
2. **Metadata Options**: Add the following to enable **tags in instance metadata**, making them accessible to Systems Manager:
   ```yaml
   MetadataOptions:
     HttpTokens: optional
     HttpPutResponseHopLimit: 2
     InstanceMetadataTags: enabled
   ```
   This allows tags to be used for identification in later stages.

### Step 2: Deploy the CloudFormation Stack
- Deploy the CloudFormation stack to create all the necessary infrastructure, including networking, EC2 instances, and RDS.
- **Verify Tags**: Ensure the **tags are enabled in metadata** to allow Systems Manager to use them for identifying instances.

### Step 3: Install CodeDeploy Agent via AWS Systems Manager (SSM)
- Use **AWS Systems Manager** to install the CodeDeploy agent on EC2 instances.
- **Run Command**: Use Systems Manager to run commands targeting the **tagged instances** (e.g., `Environment=Production`) to install the **CodeDeploy agent**.
- Alternatively, you can **install the CodeDeploy agent automatically** using UserData in the CloudFormation YAML file.

### Step 4: Create CodeDeploy Application and Deployment Group
1. **Create CodeDeploy Application**:
   - Go to AWS CodeDeploy and create an application (`MyFlaskAppDeployment`).
2. **Create Deployment Group**:
   - Create a **Deployment Group** (`MyFlaskAppGroup`) that targets instances by tag (`Environment=Production`).
   - Assign a **service role** to CodeDeploy with the necessary permissions.

### Step 5: Set Up GitHub Actions for CI/CD
1. **Create a `.github/workflows/deploy.yml`** file in your repository to define the GitHub Actions workflow:
   - **Checkout Code**: Retrieve the repository code.
   - **Set Up Python Environment**: Install dependencies.
   - **Run Tests**: Run `pytest` to verify code.
   - **Zip Source Files** for deployment.
   - **Set Up AWS Credentials** using GitHub Secrets.
   - **Upload to S3**: Use `aws s3 cp` to upload the `.zip` file to S3.
   - **Deploy with CodeDeploy**: Trigger a deployment using AWS CLI.
2. **Add Secrets to GitHub**:
   - Add `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` to **GitHub Secrets** for authentication.

## Nuances and Challenges Encountered

### 1. **S3 Bucket and Public Access**
- The initial attempt to use `--acl public-read` failed due to **"AccessControlListNotSupported"**.
- The bucket had **BlockPublicAcls** enabled, preventing ACLs like `public-read`.
- **Solution**: Remove the `--acl public-read` and use a **bucket policy** to manage public access.

### 2. **IAM Policies and Access Denied Errors**
- Several **AccessDenied** errors occurred due to missing permissions in the IAM policies.
- **Solution**: Update IAM policies for the GitHub Actions user to include the following:
  - `s3:PutObject` for uploading to S3.
  - `codedeploy:CreateDeployment`, `codedeploy:RegisterApplicationRevision`, and `s3:GetObject` for CodeDeploy.

### 3. **CodeDeploy Agent Installation**
- The **CodeDeploy agent** was not initially installed on the EC2 instance.
- **Solution**: Install the CodeDeploy agent via **AWS Systems Manager** using **Run Command** or add it to **UserData** in the CloudFormation template.

### 4. **GitHub Actions Configuration**
- The **GitHub Actions workflow** initially failed due to incorrect inputs for certain actions, like **S3 upload**.
- **Solution**: Replace the third-party action with an **AWS CLI command** to simplify and avoid unexpected input errors.

### 5. **IAM Role for EC2 Instance**
- The **IAM Role** for EC2 was configured to allow **Systems Manager** and **CodeDeploy** access.
- **Metadata Options** were enabled to allow **tags** to be visible in instance metadata for easier identification by Systems Manager.

## Final Notes and Best Practices
- **Use Bucket Policies Over ACLs**: For managing public access, using **bucket policies** is more secure and easier to manage than ACLs.
- **Centralize Access Control**: Use **IAM roles** and **policies** instead of granting permissions at the object level with ACLs.
- **Automate Everything**: Consider using **UserData** to automate tasks such as installing agents during instance launch, minimizing the need for manual intervention.
- **CI/CD with GitHub Actions**: Ensure that **AWS credentials** are securely stored in **GitHub Secrets** and that IAM roles have appropriate permissions for all services involved.

## Next Steps
- **Scaling**: Explore adding **Auto Scaling** for the EC2 instances to handle increased load seamlessly.
- **Monitoring and Alerts**: Use **CloudWatch** for monitoring and set up alarms to get notified about important metrics, such as CPU usage.
- **Blue/Green Deployments**: Implement **blue/green deployments** in CodeDeploy to reduce downtime during updates.

Feel free to contribute to the project and suggest improvements!

---
**Author**: Your Name | **Date**: [Date] | **License**: MIT License
