# File Integrity Verification using SHA-256

## Overview

This project verifies file integrity using the SHA-256 cryptographic hashing algorithm. It generates secure hashes for files and detects any unauthorized modifications by comparing current hashes with stored values.

## Features

- SHA-256 Hash Generation
- File Integrity Verification
- JSON Hash Database
- Forensic Report Generation
- Tkinter GUI

## Technologies Used

- Python
- hashlib
- JSON
- Tkinter

## Project Structure

```
csdf2/
│
├── main.py
├── hashes.json
├── Forensic_Report.txt
├── sample_files/
└── README.md
```

## Installation

No additional libraries are required.

## Run

```bash
python main.py
```

## Applications

- Digital Forensics
- Cyber Security
- Evidence Validation
- File Monitoring

## Future Enhancements

- Support multiple hashing algorithms
- Folder monitoring
- Automatic integrity alerts
- Cloud-based verification