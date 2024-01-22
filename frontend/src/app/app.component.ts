import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { DemoService } from './modules/shared/services/demo.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  title = 'frontend';

  newdata: any;

  constructor(private _apiservice: DemoService) {}

  ngOnInit(): void {
    this.getdata();
  }

  getdata() {
    this._apiservice.getDemoData().subscribe(res => {
      this.newdata = res;
    })
  }
}
