# 🔑 How to Get AWS Credentials (English Interface)

## 📋 What You Need:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY  
- AWS_REGION
- S3_BUCKET

---

## 1️⃣ AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

### Step by Step:

1. **Go to AWS Console:**
   - Open: https://console.aws.amazon.com/iam/
   - Or from main console: Click "Services" → Type "IAM" → Click on "IAM"

2. **Go to Users section:**
   - In the left menu, click **"Users"**
   - If you already have a user, click on it
   - If you don't have one, create a new one:
     - Click **"Create user"** button (usually top right)
     - **User name**: `pokeneas-user` (or any name you prefer)
     - Click **"Next"**

3. **Set Permissions:**
   - Select **"Attach policies directly"**
   - In the search box, type: `S3`
   - Check the box: **"AmazonS3FullAccess"**
   - (Optional) Also add: **"AmazonEC2ReadOnlyAccess"**
   - Click **"Next"** → **"Create user"**

4. **Create Access Keys:**
   - Click on the user you just created
   - Click on the tab **"Security credentials"** (it's near the top)
   - Scroll down to the section **"Access keys"**
   - Click **"Create access key"** button

5. **Select Use Case:**
   - Choose: **"Application running outside AWS"**
   - (Optional) Description: `For Pokeneas project`
   - Check the box at the bottom if it appears
   - Click **"Next"**

6. **⚠️ IMPORTANT - Save the Credentials:**
   - You'll see two values:
     - **Access key ID** (starts with `AKIA...`)
     - **Secret access key** (long random string)
   
   **⚠️ SAVE THESE VALUES NOW:**
   - Click **"Download .csv file"** OR copy both values
   - **You WON'T be able to see the Secret access key again** after you close this window
   - Keep them in a safe place
   - Don't share these credentials with anyone

---

## 2️⃣ AWS_REGION

### How to find your region:

1. **Go to EC2 Console:**
   - Open: https://console.aws.amazon.com/ec2/
   - Or: Click "Services" → Type "EC2" → Click on "EC2"

2. **Check your instances:**
   - Look at your instances list
   - Look at the column **"Availability Zone"**
   - Example: If it says `us-east-2c`, then your region is: **`us-east-2`**

### Common Regions:
- `us-east-1` - N. Virginia
- `us-east-2` - Ohio  
- `us-west-1` - N. California
- `us-west-2` - Oregon
- `eu-west-1` - Ireland
- `sa-east-1` - São Paulo

### You can also see it here:
- Top right corner of AWS Console shows the region name
- Example: "N. Virginia" = `us-east-1`
- Click on it to see the full list

---

## 3️⃣ S3_BUCKET

### Your bucket name:
You already know it: **`pokeneasss`**

### To verify:
1. Go to S3 Console: https://console.aws.amazon.com/s3/
2. You'll see your bucket in the list
3. Use the exact name as it appears

---

## ✅ Complete Example

Once you have everything, your variables will look like this:

```bash
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AWS_REGION="us-east-2"
export S3_BUCKET="pokeneasss"
```

---

## 🔒 Security - Best Practices

1. **Never upload these credentials to GitHub**
   - They're already in `.gitignore` so they won't be uploaded by mistake
   - Use `env.example` as a template, not `.env`

2. **Rotate credentials periodically**
   - If you think they're compromised, delete them and create new ones

3. **Use specific policies**
   - Instead of `AmazonS3FullAccess`, you can create more restrictive policies
   - Only for the bucket you need

---

## 🆘 Troubleshooting

### Error: "Invalid credentials"
- Check that you copied the credentials correctly (no extra spaces)
- Make sure the user has permissions for S3

### Error: "Access Denied" when accessing S3
- Verify the user has `AmazonS3FullAccess` or permissions on the specific bucket
- Verify the bucket name is correct

### Error: "Region mismatch"
- Make sure the bucket and instances are in the same region
