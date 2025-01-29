import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export const Navbar = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-purple-500/80 border-b border-purple-400 backdrop-blur-sm">
      <div className="container mx-auto px-4">
        <div className="h-16 flex items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <img 
              src="https://images.unsplash.com/photo-1501286353178-1ec881214838?auto=format&fit=crop&w=32&h=32" 
              alt="Website Logo" 
              className="w-8 h-8 rounded-full object-cover"
            />
            <span className="text-xl font-semibold text-white">Student News Hub</span>
          </div>
          
          <div className="flex items-center gap-4">
            <Input
              type="search"
              placeholder="Search..."
              className="w-[200px] lg:w-[300px]"
            />
            <Button variant="secondary">Login</Button>
          </div>
        </div>
      </div>
    </nav>
  );
};