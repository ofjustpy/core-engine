function    createApp() {
    jpComponentBuilder.justpyComponents.set(justpyComponents);
    console.log("justpyComponents");
    console.log(justpyComponents)
    // const allcomps = jpComponentBuilder.mount(jpComponentBuilder.App , {
    // 	target: document.getElementById("components"),
    //   })
     const allcomps = new jpComponentBuilder.App({
	 target: document.getElementById("components"),
     props: {
       name: "world",
       atag: "span",
       //justpyComponents : justpyComponents
     },
     });
  
  return allcomps;
  

}
