import { NgClass } from '@angular/common';
import { Component, input } from '@angular/core';

@Component({
    selector: 'app-cover-image',
    standalone: true,
    imports: [NgClass],
    template: `
        @defer {
            <img
                [src]="cover_image()"
                appLazyImage
                alt="{{ 'cover image for ' + name() }}"
                class="object-cover"
                [ngClass]="size()"
                style="aspect-ratio: 1 / 1.45"
            />
        } @placeholder {
            <div
                class="
                    space-y-5
                    bg-white/5 p-4
                    relative
                    before:absolute
                    before:inset-0
                    before:-translate-x-full
                    before:animate-[shimmer_2s_infinite]
                    before:bg-gradient-to-r
                    before:from-transparent
                    before:via-rose-100/10
                    before:to-transparent
                    isolate
                    overflow-hidden
                    shadow-xl
                    shadow-black/5
                    before:border-t
                    before:border-rose-100/10"
                [ngClass]="size()"
                style="aspect-ratio: 1 / 1.45"
            ></div>
            <div
                class="
                    bg-gradient-to-r
                    from-transparent
                    via-rose-100/10
                    to-transparent
                    -translate-x-full
                    animate-[shimmer_2s_infinite]"
            ></div>
        }
    `
})
export class CoverImageComponent {
    cover_image = input.required();
    name = input.required();
    size = input('w-full');
}
