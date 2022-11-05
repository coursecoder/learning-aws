pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: '129377ef-f160-4161-b13f-f8310482ccdb',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                        //clone git repo
                        //sh 'git init'
                        //sh 'git remote add origin https://github.com/Fullstack-Playdough-Team/Team-Playdough.git'
                        //sh 'git pull origin main'
                        script {
                            def bucket_name = "test-leaderboard"
                            //sh "/usr/local/bin/aws s3api create-bucket --bucket ${bucket_name} --region us-east-1"
                            //sh "/usr/local/bin/aws s3 website s3://${bucket_name}/ --index-document index.html"
                            // update bucket policy with bucket name
                            def FILE_PATH_1 = "./resources/s3_policy.json"
                            sh "sed -i 's/<bucket_name>/${bucket_name}/g' ${FILE_PATH_1}"                       
                            
                            // update python script with bucket name
                            def FILE_PATH_2 = "./resources/put_bucket_policy.py"
                            sh "sed -i 's/<bucket_name>/${bucket_name}/g' ${FILE_PATH_2}"   
                            
                            // run script to attach bucket policy to S3 bucket
                            sh "python3 ./resources/put_bucket_policy.py"

                            // copy files to S3 bucket
                            sh "/usr/local/bin/aws s3 cp ./resources/website s3://${bucket_name}/ --recursive --cache-control 'max-age=0'"
                            
                            // create DynamoDB table
                            sh "python3 ./resources/create_table.py"

                            // batch upload gamers to DynamoDB table
                            sh "python3 ./python_3/batch_put.py"

                            // add Global Secondary Index to DynamoDB table
                            sh "python3 ./python_3/add_gsi.py"

                            // copy lambda functions to S3 bucket
                            sh "/usr/local/bin/aws s3 cp ./python_3/get_all_leaderboard_code.zip s3://${bucket_name}/ --cache-control 'max-age=0'"
                            sh "/usr/local/bin/aws s3 cp ./python_3/submit_score_code.zip s3://${bucket_name}/ --cache-control 'max-age=0'"

                            // create IAM role and GET Lambda 
                            sh "python3 ./python_3/create_iam_and_lambda.py"

                            // create LeaderBoardAPI and create /leaderboard endpoint
                            sh "python3 ./python_3/create_leaderboard_api.py"

                            // create /leaderboard/top_gamer endpoint
                            sh "python3 ./python_3/create_top_gamer_api.py"

                            // create POST lambda
                            sh "python3 ./python_3/create_submit_lambda.py"

                            // create and deploy /score/submit POST endpoint
                            sh "python3 ./python_3/create_submit_score_api.py"
                        }
                    }
            }
        }
        stage('Test') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: '129377ef-f160-4161-b13f-f8310482ccdb',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                        script {
                            // test bucket creation
                            sh '/usr/local/bin/aws s3 ls' 

                            // test endpoint functionality
                            def api_url = "$(python3 ./python_3/get_api_url.py)"
                            sh "curl --request GET '${api_url}/leaderboard/top_gamer'"
                        }
                }
            }
        }
        stage('Deploy') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: '129377ef-f160-4161-b13f-f8310482ccdb',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                        
                        def FILE_PATH_3 = "./resources/website/config.js"
                        def api_url = "$(python3 ./python_3/get_api_url.py)"
                        echo \"${api_url}\"
                        sh "sed -i '0,/null/{s,null,\"${api_url}\",g}' ${FILE_PATH_3}"
                        // upload config.js file with API Gateway invoke url to S3 bucket
                        python3 ./python_3/update_config.py

                        sh "echo 'Your game website and leaderboard is now available on AWS!'"
                        echo 'https://${bucket_name}.s3.amazonaws.com/index.html'
                }
            }
        }
    }
}