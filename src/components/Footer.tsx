import { Facebook, Twitter, Instagram, Youtube } from "lucide-react";

export const Footer = () => {
  return (
    <footer className="bg-primary text-primary-foreground mt-20">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="font-bold text-lg mb-4">About Us</h3>
            <p className="text-sm opacity-80">
              Your trusted source for the latest student news and updates from across all academic fields.
            </p>
          </div>
          <div>
            <h3 className="font-bold text-lg mb-4">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li>Home</li>
              <li>News</li>
              <li>Events</li>
              <li>Contact</li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold text-lg mb-4">Contact Us</h3>
            <ul className="space-y-2 text-sm">
              <li>Email: info@studentnews.com</li>
              <li>Phone: (555) 123-4567</li>
              <li>Address: 123 Campus Drive</li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold text-lg mb-4">Follow Us</h3>
            <div className="flex gap-4">
              <Facebook className="w-5 h-5" />
              <Twitter className="w-5 h-5" />
              <Instagram className="w-5 h-5" />
              <Youtube className="w-5 h-5" />
            </div>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-primary-foreground/20 text-center text-sm opacity-80">
          © 2024 StudentNews. All rights reserved.
        </div>
      </div>
    </footer>
  );
};