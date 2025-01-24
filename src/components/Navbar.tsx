import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { LogIn, Search } from "lucide-react";

export const Navbar = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 bg-white/90 backdrop-blur-sm z-50 border-b">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <img src="https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=50&h=50&fit=crop" alt="Logo" className="w-10 h-10 rounded-full object-cover" />
          <span className="font-bold text-xl text-primary">StudentNews</span>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="relative hidden sm:flex items-center">
            <Input
              type="search"
              placeholder="Search news..."
              className="w-[200px] lg:w-[300px] pr-8"
            />
            <Search className="w-4 h-4 absolute right-3 text-muted-foreground" />
          </div>
          
          <Button className="flex items-center gap-2">
            <LogIn className="w-4 h-4" />
            Login
          </Button>
        </div>
      </div>
    </nav>
  );
};