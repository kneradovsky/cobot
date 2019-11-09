import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { LocationsComponent } from './locations/locations.component';
import { AuthGuard } from './auth.guard';
import { UserComponent } from './user/user.component';
import { EventsComponent } from './events/events.component';
import { EventrequestComponent } from './eventrequest/eventrequest.component';


const routes: Routes = [
  {path: '', component: LocationsComponent, canActivate: [AuthGuard]},
  {path: 'locations', component: LocationsComponent, canActivate: [AuthGuard]},
  {path: 'login', component: LoginComponent},
  {path: 'users', component: UserComponent, canActivate: [AuthGuard]},
  {path: 'events', component: EventsComponent, canActivate: [AuthGuard]},
  {path: 'eventreqs', component: EventrequestComponent, canActivate: [AuthGuard]}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
