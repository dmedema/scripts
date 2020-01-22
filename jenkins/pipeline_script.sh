node {
    stage('Scm Checkout'){
        git credentialsID: 'git-creds', url: 'https://github.com/javahometech/my-app'
    }
    stage('Mvn Package'){
        def mvnHome = tool name: 'maven-3', type: 'maven'
        def mvnCMD = "${mvnHome}/bin/mvn"
        sh "${mvnCMD} clean package"
    }
    stage('Build Docker Image'){
        # Docker needs to be installed on Jenkins server
        # Also Jenkins user needs permissions to run docker commands
        sh 'docker build -t dmedema/my-app:2.0.0 .'
    }
    stage('Push Docker Image'){
        # Bind credentials in Jenkins and add a credential
        # Call it dockerHubPwd use Secret text for the credential
        # docker-pwd
        withCredentials([string(credentialsId: 'docker-pwd', variable: 'dockerHubPwd')]){
            sh "docker login -u dmedema -p ${dockerHubPwd}"
        }
        sh 'docker push dmedema/my-app:2.0.0'
    }
    stage('RunContainer on Dev Server'){
        # Install sshAgent (SSH Agent Plugin)on the Jenkins server
        # and create a variable with your pem file. Username with private key
        # If you run this a second time you must terminate the previous docker
        # instance or docker will try to run on port 8080 again and there will
        # be already be a docker running on port 8080
        def dockerRun = 'docker run -p 8080:8080 -d --name my-app dmedema/my-app:2.0.0'
        sshagent(['dev-server']){
            sh "ssh -o StrictHostKeyChecking=no ec2-user@PublicIP ${dockerRun}"
        }
    }
}
