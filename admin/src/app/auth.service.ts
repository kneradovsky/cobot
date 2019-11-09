import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {map} from 'rxjs/operators';
import { ConfigService } from './config.service';

const tokenVar = 'access_token';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private cfg: ConfigService, private http: HttpClient) { }

  login(username: string, password: string): Observable<boolean> {
    return this.http.post<{user: string, token: string}>(this.cfg.apiUrl + '/auth',{user:{username: username,password:password}})
    .pipe(
      map(res => {
        localStorage.setItem(tokenVar, res.token);
        console.log(`user ${res.user} logged in`);
        return true;
      })
    );
  }

  logout() {
    localStorage.removeItem(tokenVar);
  }

  public get loggedIn() {
    return localStorage.getItem(tokenVar) != null;
  }
}
