import { Injectable } from '@angular/core';
import { CUser} from './user';
import { ConfigService } from './config.service';
import { HttpBackend, HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private cfg: ConfigService,private http :HttpClient) { }

  public get list() {
    return this.http.get<Array<CUser>>(this.cfg.apiUrl+'/users');
  }

  public update(inuser: CUser) {
    return this.http.post<{updated: number}>(this.cfg.apiUrl + '/users', { user:  inuser});
  }

  public delete(inuser: CUser) {
    return this.http.request<{deleted: number}>('DELETE', this.cfg.apiUrl + '/users', {body: { user:  inuser}});
  }
}
