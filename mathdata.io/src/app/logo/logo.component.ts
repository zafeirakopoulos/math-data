import { Component, OnInit, Input } from '@angular/core';
import { SafeStyle, DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-logo',
  templateUrl: './logo.component.html',
  styleUrls: ['./logo.component.css']
})
export class LogoComponent implements OnInit {
  @Input() fontSize: string;
  _fontSize: SafeStyle;

  constructor(private _sanitizer: DomSanitizer) {
  }

  ngOnInit() {
    this._fontSize = this._sanitizer.bypassSecurityTrustStyle(this.fontSize);
  }

}
