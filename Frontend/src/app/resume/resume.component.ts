import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-resume',
  templateUrl: './resume.component.html',
  styleUrls: ['./resume.component.css']
})
export class ResumeComponent implements OnInit {
  resumes: any[] = [];
  resumeTitle: string = '';
  selectedFile: File | null = null;
  apiUrl = `${environment['apiBaseUrl']}/api/resumes`; // Update with actual API

  constructor(private http: HttpClient, private modalService: NgbModal) {}

  ngOnInit() {
    this.loadResumes();
  }

  // Load resumes from API
  loadResumes() {
    this.http.get<any[]>(this.apiUrl).subscribe(res => {
      this.resumes = res;
    });
  }

  // Open modal for uploading resume
  openUploadModal() {
    const modalElement = document.getElementById('uploadModal');
    if (modalElement) {
      const modal = new bootstrap.Modal(modalElement);
      modal.show();
    }
  }

  // Handle file selection
  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  // Upload resume
  uploadResume() {
    if (!this.selectedFile || !this.resumeTitle) {
      alert('Please select a file and enter a title.');
      return;
    }

    const formData = new FormData();
    formData.append('title', this.resumeTitle);
    formData.append('file', this.selectedFile);

    this.http.post(this.apiUrl, formData).subscribe(() => {
      alert('Resume uploaded successfully!');
      this.loadResumes();
      this.closeModal();
    });
  }

  // Delete resume
  deleteResume(id: number) {
    if (confirm('Are you sure you want to delete this resume?')) {
      this.http.delete(`${this.apiUrl}/${id}`).subscribe(() => {
        alert('Resume deleted successfully!');
        this.loadResumes();
      });
    }
  }

  // Close modal
  closeModal() {
    const modalElement = document.getElementById('uploadModal');
    if (modalElement) {
      const modal = bootstrap.Modal.getInstance(modalElement);
      modal?.hide();
    }
  }
}