
package com.creatoriq.controller;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/wallet")
public class WalletController {
    @GetMapping("/health")
    public String health(){
        return "ok";
    }

    @GetMapping("/{id}")
    public String getWallet(@PathVariable String id){
        return "Wallet for " + id;
    }
}
