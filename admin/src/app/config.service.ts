import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ConfigService {
  public apiUrl = 'http://84.201.173.78:8080/api';
  constructor() { }
}
