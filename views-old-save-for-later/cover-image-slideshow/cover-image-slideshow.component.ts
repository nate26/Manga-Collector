import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ICoverImage } from '../../src/app/interfaces/iVolume.interface';

@Component({
    selector: 'app-cover-image-slideshow',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './cover-image-slideshow.component.html',
    styleUrl: './cover-image-slideshow.component.css'
})
export class CoverImageSlideshowComponent {

    @Input() cover!: ICoverImage[];
    @Input() title!: string;

    getCover() {
        return this.cover.sort((a) => a.name === 'primary' ? -1 : 1)[0].url.replace('www', 'legacy');
    }

}
