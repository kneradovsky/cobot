import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { JwtModule } from '@auth0/angular-jwt';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule} from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import {AuthService} from './auth.service';
import {AuthGuard} from './auth.guard';
import {ConfigService} from './config.service';
import {LocationsService} from './locations.service';
import { LocationsComponent } from './locations/locations.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { UserComponent } from './user/user.component';

export function tokenGetter() {
  return localStorage.getItem('access_token');
}

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    LocationsComponent,
    UserComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    JwtModule.forRoot({
      config: {
        tokenGetter: tokenGetter,
        whitelistedDomains: ['localhost:4000'],
        blacklistedRoutes: ['localhost:4000/api/auth']
      }
    }),
    HttpClientModule,
    FormsModule,
    BrowserAnimationsModule,
    NgbModule,
  ],
  providers: [
    AuthService,
    AuthGuard,
    ConfigService,
    LocationsService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
