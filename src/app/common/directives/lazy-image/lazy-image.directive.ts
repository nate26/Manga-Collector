import { Directive, ElementRef } from '@angular/core';

@Directive({
  selector: '[appLazyImage]',
  standalone: true
})
export class LazyImageDirective {
  constructor({ nativeElement }: ElementRef<HTMLImageElement>) {
    if ('loading' in HTMLImageElement.prototype) {
      nativeElement.setAttribute('loading', 'lazy');
    } else {
      // TODO other browser support?
    }
  }
}
