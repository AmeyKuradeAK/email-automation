const express = require('express');
const multer = require('multer');
const cors = require('cors');
const crypto = require('crypto');
const nodemailer = require('nodemailer');
const path = require('path');
const fs = require('fs');

const app = express();
const port = process.env.PORT || 5000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors({ origin: 'https://email-automation-frontend-mu.vercel.app/' }));  // Adjust the origin to match your frontend URL

// Set up multer storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const dir = './uploads';
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir);
    }
    cb(null, dir);
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname));
  }
});

const upload = multer({ storage });

// Upload route
app.post('/upload', upload.fields([{ name: 'markdown' }, { name: 'csv' }]), (req, res) => {
  console.log('Received files:', req.files);
  const { markdown, csv } = req.files;

  // Function to generate hash of the file
  const generateFileHash = (filePath) => {
    const hash = crypto.createHash('sha256');
    const fileStream = fs.createReadStream(filePath);
    fileStream.on('data', (chunk) => hash.update(chunk));
    return new Promise((resolve, reject) => {
      fileStream.on('end', () => resolve(hash.digest('hex')));
      fileStream.on('error', (err) => reject(err));
    });
  };

  const sendEmailNotification = async () => {
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.GMAIL_USER, 
        pass: process.env.GMAIL_PASS 
      }
    });

    const mailOptions = {
      from: process.env.GMAIL_USER,
      to: 'recipient@example.com',
      subject: 'File Upload Successful',
      text: 'Your files have been uploaded successfully.'
    };

    try {
      await transporter.sendMail(mailOptions);
      console.log('Email sent successfully');
    } catch (err) {
      console.error('Email sending failed:', err);
    }
  };

  const processFiles = async () => {
    try {
      const markdownFileHash = await generateFileHash(markdown[0].path);
      const csvFileHash = await generateFileHash(csv[0].path);

      await sendEmailNotification();

      res.json({
        success: true,
        message: 'Files uploaded successfully',
        files: {
          markdown: {
            originalName: markdown[0].originalname,
            size: markdown[0].size,
            hash: markdownFileHash
          },
          csv: {
            originalName: csv[0].originalname,
            size: csv[0].size,
            hash: csvFileHash
          }
        }
      });
    } catch (err) {
      console.error('Error processing files:', err);
      res.status(500).json({ error: 'Internal server error' });
    }
  };

  processFiles();
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
