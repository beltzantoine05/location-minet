import { Link } from 'react-router-dom'
import Logo from '@/assets/minet_light.png'


export default function Footer() {
    return (
        <footer className="border-t bg-muted/20">
            <div className="container mx-auto px-4 max-w-7xl py-8 md:py-12">
                <img src={Logo} alt="logo" className="w-16 h-16" />
                <div className="flex flex-col items-center justify-between gap-4 md:flex-row">

                    <div className="flex flex-col items-center gap-2 md:items-start text-center md:text-left">
                        <span className="font-bold text-lg">Location</span>
                        <p className="text-sm text-muted-foreground">
                            La plateforme de prêt de matériel inter-associations.
                        </p>
                    </div>

                    <div className="flex gap-4 text-sm text-muted-foreground">
                        <Link to="/mentions" className="hover:text-primary transition-colors hover:underline">
                            Mentions Légales
                        </Link>
                        <Link to="/contact" className="hover:text-primary transition-colors hover:underline">
                            Contact
                        </Link>
                    </div>

                </div>

                <div className="mt-8 border-t pt-8 text-center text-xs text-muted-foreground">
                    © {new Date().getFullYear()} MiNET. Tous droits réservés.
                    <br />
                    Developpé et designé par Antoine Beltz
                </div>
            </div>
        </footer>
    )
}
