import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { LoginComponent } from './login/login.component';
import { LogoutComponent } from './logout/logout.component';
import { AuthGuard } from './_auth/guards/auth.guard';
import { RegisterComponent } from './register/register.component';
import { JobComponent } from './job/job.component';

const routes: Routes = [
  { path: 'dashboard', component: DashboardComponent , canActivate: [AuthGuard] },
  { path: 'job-list', component: JobComponent , canActivate: [AuthGuard] },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'logout', component: LogoutComponent },
  { path: '**', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: '',  redirectTo: '/dashboard', pathMatch: 'full' }, // catch all route
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
