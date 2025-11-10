# Anki Font Resizer

This Anki-add-on allows to adjust the text size on the front and back of each card. Three buttons, *A+*, *A-* and *A (delete)*, are added to the interface. When text is selected, its size can be increased or decreased by 10%, with a minimum of 50% and a maximum of 400%.

## Testing

To test this add-on just copy the files into `C:\Users\home\AppData\Roaming\Anki2\addons21\anki_font_resizer`. Start Anki, add the add-on, if you don't have it already added and open the card management view.

## Contribution

Contributions are welcome!  
To submit a Pull Request:
1. Fork this repository
2. Create a new branch (`git checkout -b feature/my-change`)
4. Commit and push your changes
5. Open a Pull Request

Please include a short description of what you changed and why.

## Developstate

The following issues are currently known:

- When resizing a selected text that occurs multiple times, only the first occurrence is affected
- After each action the selected text is no longer selected
