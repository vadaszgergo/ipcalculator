# Deployment Guide for IP Tools Suite

## Quick Overview
Your Flask application is ready to deploy with multiple options. All necessary files have been created.

## Option 1: Docker Deployment (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- Domain or server IP

### Steps
1. **Upload files to your server:**
   ```bash
   scp -r . user@your-server:/home/user/ip-tools-suite/
   ```

2. **Build and run with Docker:**
   ```bash
   cd ip-tools-suite
   docker-compose up -d
   ```

3. **Access your application:**
   - Visit `http://your-server-ip:5000`

## Option 2: Traditional VPS/Server Deployment

### Prerequisites
- Ubuntu/Debian server with sudo access
- Python 3.11+

### Steps
1. **Upload files to server:**
   ```bash
   scp -r . user@your-server:/tmp/ip-tools-suite/
   ```

2. **Run deployment script:**
   ```bash
   ssh user@your-server
   cd /tmp/ip-tools-suite
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Set up reverse proxy (optional but recommended):**
   ```bash
   sudo apt install nginx
   sudo cp nginx.conf /etc/nginx/sites-available/ip-tools
   sudo ln -s /etc/nginx/sites-available/ip-tools /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Option 3: Cloud Platform Deployments

### AWS (using Elastic Beanstalk)
1. Install AWS CLI and EB CLI
2. Initialize: `eb init`
3. Create environment: `eb create ip-tools-prod`
4. Deploy: `eb deploy`

### Google Cloud Platform (using Cloud Run)
1. Build image: `gcloud builds submit --tag gcr.io/PROJECT-ID/ip-tools`
2. Deploy: `gcloud run deploy --image gcr.io/PROJECT-ID/ip-tools --port 5000`

### Azure (using Container Instances)
1. Build image: `az acr build --registry myregistry --image ip-tools .`
2. Deploy: `az container create --resource-group myRG --name ip-tools --image myregistry.azurecr.io/ip-tools`

### DigitalOcean App Platform
1. Connect your GitHub repository
2. Select "Web Service" 
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `gunicorn --bind 0.0.0.0:$PORT main:app`

## Option 4: Shared Hosting (cPanel/WHM)

For shared hosting with Python support:

1. **Upload files via File Manager or FTP**
2. **Create Python app in cPanel:**
   - Python version: 3.11
   - Application root: `/public_html/ip-tools`
   - Application URL: your-domain.com/ip-tools
   - Application startup file: `main.py`
3. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

## Security Considerations

### Environment Variables
Set these in production:
- `FLASK_ENV=production`
- `SECRET_KEY=your-secret-key` (generate a secure random key)

### Firewall
Only open necessary ports:
```bash
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### SSL Certificate (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Monitoring and Maintenance

### Check application status:
```bash
sudo systemctl status ip-tools
```

### View logs:
```bash
sudo journalctl -u ip-tools -f
```

### Update application:
1. Upload new files
2. Restart service: `sudo systemctl restart ip-tools`

## Estimated Costs

### VPS Options:
- **DigitalOcean Droplet:** $6-12/month (1-2GB RAM)
- **AWS Lightsail:** $5-10/month
- **Linode:** $5-10/month
- **Vultr:** $6-12/month

### Managed Options:
- **Heroku:** Free tier available, $7/month for hobby plan
- **Railway:** $5/month
- **Render:** Free tier available

## Domain Setup

1. **Purchase domain** (Namecheap, Cloudflare, etc.)
2. **Point A record** to your server IP
3. **Update nginx.conf** with your domain name
4. **Get SSL certificate** with Let's Encrypt

Your application will be production-ready with any of these deployment methods!