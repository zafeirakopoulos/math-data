import { Component, OnInit } from '@angular/core';
import { SafeStyle, DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.css']
})
export class LandingPageComponent implements OnInit {
  features = [
    {
      icon: 'star',
      name: 'Feature 1',
      lines: ['Lorem ipsum dolor sit amet consectetur, adipisicing elit. Id nemo modi qui enim, sapiente ex officiis nostrum provident, fuga quibusdam est. Libero earum repellat ad eaque nisi architecto magnam magni.']
    }, {
      icon: 'folder',
      name: 'Feature 2',
      lines: ['Lorem ipsum dolor sit amet consectetur, adipisicing elit. Id nemo modi qui enim, sapiente ex officiis nostrum provident, fuga quibusdam est. Libero earum repellat ad eaque nisi architecto magnam magni.']
    }, {
      icon: 'note',
      name: 'Feature 3',
      lines: ['Lorem ipsum dolor sit amet consectetur, adipisicing elit. Id nemo modi qui enim, sapiente ex officiis nostrum provident, fuga quibusdam est. Libero earum repellat ad eaque nisi architecto magnam magni.']
    },
  ];
  constructor(private _sanitizer: DomSanitizer) { }

  ngOnInit() {
  }

  scrollTo(element: string) {
    const pos = document.querySelector(element).getBoundingClientRect();
    console.log(pos);
    window.scrollTo({top: pos.top - 64, left: 0, behavior: 'smooth'})
  }
}
