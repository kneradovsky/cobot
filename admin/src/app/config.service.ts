import { Injectable } from '@angular/core';
import { environment} from './../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ConfigService {
  public apiUrl = 'http://84.201.173.78:8080/api';
  constructor() {
    if (environment.production) {
      this.apiUrl = '/api';
    }
   }
}
