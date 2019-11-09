import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { LocationsComponent } from './locations/locations.component';
import { AuthGuard } from './auth.guard';


const routes: Routes = [
  {path: 'locations', component: LocationsComponent, canActivate: [AuthGuard]},
  {path: 'login', component: LoginComponent},


];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
