pipeline {
    agent any
    stages {
        stage('1. Checkout Code') {
            steps {
                script {
                    // Xóa dữ liệu cũ để đảm bảo kéo code mới nhất không bị xung đột
                    deleteDir()
                    // Cấu hình bỏ qua SSL nếu mạng chập chờn
                    sh 'git config --global http.sslVerify false'
                    git branch: 'main', url: 'https://github.com/MaTuyetNgaHCMUS/MMTNC-DevSecOp.git'
                }
            }
        }
        
        stage('2. SAST Scan (Bandit)') {
            steps {
                echo '--- Đang quét mã nguồn tĩnh (SAST) ---'
                // Sử dụng python3 -m bandit để Jenkins luôn tìm thấy công cụ
                sh 'python3 -m bandit -r . -f txt -o report_sast.txt || true'
            }
        }

        stage('3. DAST Scan (Nmap/ZAP)') {
            steps {
                echo '--- Đang quét bảo mật động (DAST) ---'
                // nohup giúp chạy app ngầm để Nmap có cái để quét mà không làm dừng Pipeline
                sh 'nohup python3 app.py & sleep 5 && nmap -F localhost > report_dast.txt || true'
            }
        }
    }
    post {
        always {
            // Lưu lại báo cáo để có minh chứng nộp bài (Artifacts)
            archiveArtifacts artifacts: 'report_sast.txt, report_dast.txt', allowEmptyArchive: true
        }
    }
}