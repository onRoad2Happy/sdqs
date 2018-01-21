def evaluate(id, cpu, memory, platform, instance, region, zone, amount, duration):
    cpu = cpu * amount
    memory = memory * amount

    type_price_variance = suggest_types(region, zone, cpu, memory, instance, duration)







