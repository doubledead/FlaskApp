import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class DemoService {

  constructor(private _http: HttpClient) { }

  getDemoData() {
    return this._http.get('http://127.0.0.1:5000/api/');
  }
}
