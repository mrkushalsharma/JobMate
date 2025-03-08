import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
// import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { environment } from 'src/environments/environment';
import { AuthService } from '../_auth/services/auth.service';
import { NgxSpinnerService } from 'ngx-spinner';

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
  showModal = false;
  formSubmitted: boolean = false;

  constructor(private authService: AuthService,
    private spinner: NgxSpinnerService,
    private http: HttpClient) { }

  ngOnInit() {
    this.loadResumes();
  }

  // Load resumes from API
  loadResumes() {
    this.http.get(environment['apiBaseUrl'] + 'resumes/', {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${this.authService.getToken()}`,
        'Content-Type': 'application/json'
      })
    }).subscribe((response: any) => {
      if(response?.length){
        this.resumes = response;
      }
      // this.datas = response;
    }, err => {
      console.log(err)
    });
  }

  // Open modal for uploading resume
  openUploadModal() {
    this.showModal = true;
  }

  closeUploadModal() {
    this.showModal = false;
  }

  // Handle file selection
  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  // Upload resume
  uploadResume() {
    this.formSubmitted = true;
    if (!this.selectedFile || !this.resumeTitle) {
      return;
    }

    const formData = new FormData();
    formData.append('title', this.resumeTitle);
    formData.append('file', this.selectedFile);

    this.http.post(environment['apiBaseUrl'] + 'resumes/', formData, {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${this.authService.getToken()}`,
        // 'Content-Type': 'application/json'
      }, )
    }).subscribe(response => {
      this.closeUploadModal();
      this.loadResumes();
    }, err => {
      console.log(err)
    });
  }

  // Delete resume
  deleteResume(id: number) {
    if (confirm('Are you sure you want to delete this resume?')) {
      this.http.delete(`${environment['apiBaseUrl']}resumes/${id}`, {
        headers: new HttpHeaders({
          'Authorization': `Bearer ${this.authService.getToken()}`,
          'Content-Type': 'application/json'
        })
      }).subscribe(response => {
        this.loadResumes();
      }, err => {
        console.log(err)
      });
    }
  }

}