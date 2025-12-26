# Buat file app.py lengkap dengan CRUD
cat > app.py << 'EOF'
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sekolah.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Siswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nis = db.Column(db.String(20), unique=True)
    nama = db.Column(db.String(100))
    kelas = db.Column(db.String(10))
    alamat = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nis': self.nis,
            'nama': self.nama,
            'kelas': self.kelas,
            'alamat': self.alamat
        }

# Create database tables
with app.app_context():
    db.create_all()
    
    # Add sample data if empty
    if Siswa.query.count() == 0:
        siswa1 = Siswa(nis='2023001', nama='Budi Santoso', kelas='XII IPA 1', alamat='Jl. Merdeka No. 10')
        siswa2 = Siswa(nis='2023002', nama='Siti Aminah', kelas='XII IPA 1', alamat='Jl. Sudirman No. 45')
        db.session.add(siswa1)
        db.session.add(siswa2)
        db.session.commit()

# ========== API ROUTES ==========

@app.route('/')
def home():
    return '''
    <h1>Sistem Manajemen Sekolah - Ubuntu VM</h1>
    <p>Deployment berhasil di Virtual Machine!</p>
    <a href="/api/siswa">View API Data</a><br>
    <a href="/dashboard">Dashboard</a>
    '''

@app.route('/dashboard')
def dashboard():
    total = Siswa.query.count()
    return f'''
    <h1>Dashboard</h1>
    <p>Total Siswa: {total}</p>
    <a href="/api/siswa">API Data</a><br>
    <a href="/">Home</a>
    '''

@app.route('/api/siswa', methods=['GET'])
def get_all_siswa():
    siswa_list = Siswa.query.all()
    return jsonify([s.to_dict() for s in siswa_list])

@app.route('/api/siswa/<int:id>', methods=['GET'])
def get_siswa(id):
    siswa = Siswa.query.get_or_404(id)
    return jsonify(siswa.to_dict())

@app.route('/api/siswa', methods=['POST'])
def create_siswa():
    data = request.json
    new_siswa = Siswa(
        nis=data['nis'],
        nama=data['nama'],
        kelas=data['kelas'],
        alamat=data.get('alamat', '')
    )
    db.session.add(new_siswa)
    db.session.commit()
    return jsonify({'message': 'Siswa berhasil ditambahkan', 'id': new_siswa.id}), 201

@app.route('/api/siswa/<int:id>', methods=['PUT'])
def update_siswa(id):
    siswa = Siswa.query.get_or_404(id)
    data = request.json
    
    if 'nama' in data:
        siswa.nama = data['nama']
    if 'kelas' in data:
        siswa.kelas = data['kelas']
    if 'alamat' in data:
        siswa.alamat = data['alamat']
    
    db.session.commit()
    return jsonify({'message': 'Siswa berhasil diupdate'})

@app.route('/api/siswa/<int:id>', methods=['DELETE'])
def delete_siswa(id):
    siswa = Siswa.query.get_or_404(id)
    db.session.delete(siswa)
    db.session.commit()
    return jsonify({'message': 'Siswa berhasil dihapus'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
EOF

# Verifikasi
cat app.py
