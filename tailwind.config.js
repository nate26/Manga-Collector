/** @type {import('tailwindcss').Config} */

var plugin = require('tailwindcss/plugin');

module.exports = {
    content: [
        './src/**/*.{html,ts}'
    ],
    theme: {
        extend: {
            textShadow: {
                DEFAULT: '0px 0px 5px var(--tw-shadow-color)'
            }
        }
    },
    plugins: [
        plugin(function ({ matchUtilities, theme }) {
            matchUtilities(
                {
                    'text-shadow': (value) => ({
                        textShadow: value,
                    }),
                },
                { values: theme('textShadow') }
            )
        })
    ]
};
